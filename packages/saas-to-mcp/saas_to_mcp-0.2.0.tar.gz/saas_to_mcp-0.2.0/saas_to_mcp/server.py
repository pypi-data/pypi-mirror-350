"""
Main SaasToMCP server implementation.

This module provides the core server functionality for converting web APIs
into MCP (Model Context Protocol) tools.
"""

import json
import asyncio
import inspect
from typing import Dict, Any, Optional, List, Union
from urllib.parse import urljoin, quote
import httpx
from fastmcp import FastMCP, Context
from .models import APIConfig, APIEndpoint, AuthConfig, RequestParam


class SaasToMCP:
    """Main server that creates MCP tools from API configurations."""
    
    def __init__(self, name: str = "SaasToMCP"):
        self.mcp = FastMCP(name)
        self.apis: Dict[str, APIConfig] = {}
        self.http_clients: Dict[str, httpx.AsyncClient] = {}
        self._setup_core_tools()
    
    def _setup_core_tools(self):
        """Set up the core management tools."""
        
        @self.mcp.tool()
        async def register_api(config: Dict[str, Any], ctx: Context) -> str:
            """
            Register a new API configuration and create MCP tools for its endpoints.
            
            Args:
                config: API configuration dictionary containing:
                    - name: API name
                    - base_url: Base URL for the API
                    - description: Optional API description
                    - auth: Optional authentication configuration
                    - headers: Optional global headers
                    - endpoints: List of endpoint configurations
            
            Returns:
                Success message with list of created tools
            """
            try:
                api_config = APIConfig(**config)
                
                # Store API configuration
                self.apis[api_config.name] = api_config
                
                # Create HTTP client for this API
                client = await self._create_http_client(api_config)
                self.http_clients[api_config.name] = client
                
                # Create tools for each endpoint
                created_tools = []
                for endpoint in api_config.endpoints:
                    tool_name = f"{api_config.name}_{endpoint.name}"
                    try:
                        await self._create_endpoint_tool(api_config, endpoint, tool_name)
                        created_tools.append(tool_name)
                    except Exception as e:
                        await ctx.error(f"Failed to create tool {tool_name}: {str(e)}")
                        continue
                
                await ctx.info(f"Registered API '{api_config.name}' with {len(created_tools)} tools")
                return f"Successfully registered API '{api_config.name}' with tools: {', '.join(created_tools)}"
                
            except Exception as e:
                await ctx.error(f"Failed to register API: {str(e)}")
                raise
        
        @self.mcp.tool()
        async def list_apis(ctx: Context) -> Dict[str, Any]:
            """
            List all registered APIs and their endpoints.
            
            Returns:
                Dictionary of registered APIs with their configurations
            """
            result = {}
            for name, api in self.apis.items():
                result[name] = {
                    "base_url": api.base_url,
                    "description": api.description,
                    "auth_type": api.auth.type if api.auth else "none",
                    "endpoints": [
                        {
                            "name": ep.name,
                            "method": ep.method,
                            "path": ep.path,
                            "description": ep.description,
                            "parameters": [
                                {
                                    "name": param.name,
                                    "type": param.type,
                                    "location": param.location,
                                    "required": param.required,
                                    "description": param.description,
                                    "default": param.default
                                }
                                for param in ep.params
                            ]
                        }
                        for ep in api.endpoints
                    ]
                }
            return result
        
        @self.mcp.tool()
        async def unregister_api(api_name: str, ctx: Context) -> str:
            """
            Unregister an API and remove its tools.
            
            Args:
                api_name: Name of the API to unregister
            
            Returns:
                Success message
            """
            if api_name not in self.apis:
                raise ValueError(f"API '{api_name}' not found")
            
            api_config = self.apis[api_name]
            
            # Remove tools
            for endpoint in api_config.endpoints:
                tool_name = f"{api_name}_{endpoint.name}"
                try:
                    self.mcp.remove_tool(tool_name)
                except:
                    pass  # Tool might not exist
            
            # Close HTTP client
            if api_name in self.http_clients:
                await self.http_clients[api_name].aclose()
                del self.http_clients[api_name]
            
            # Remove API config
            del self.apis[api_name]
            
            await ctx.info(f"Unregistered API '{api_name}'")
            return f"Successfully unregistered API '{api_name}'"
        
        @self.mcp.tool()
        async def test_api_connection(api_name: str, ctx: Context) -> Dict[str, Any]:
            """
            Test connection to a registered API.
            
            Args:
                api_name: Name of the API to test
            
            Returns:
                Connection test results
            """
            if api_name not in self.apis:
                raise ValueError(f"API '{api_name}' not found")
            
            api_config = self.apis[api_name]
            client = self.http_clients.get(api_name)
            
            if not client:
                raise ValueError(f"No HTTP client found for API '{api_name}'")
            
            try:
                # Try a simple HEAD or GET request to base URL
                response = await client.head(api_config.base_url, timeout=5.0)
                return {
                    "status": "connected",
                    "status_code": response.status_code,
                    "headers": dict(response.headers)
                }
            except Exception as e:
                return {
                    "status": "failed",
                    "error": str(e)
                }
        
        @self.mcp.tool()
        async def call_api(
            api_name: str,
            endpoint_name: str,
            parameters: Dict[str, Any] = None,
            ctx: Optional[Context] = None
        ) -> Dict[str, Any]:
            """
            Call any registered API endpoint with dynamic parameters.
            
            This is a generic tool that allows calling any registered API endpoint
            without having to use the specific endpoint tools. Useful for ad-hoc
            API calls or when you want more flexibility.
            
            Args:
                api_name: Name of the registered API to call
                endpoint_name: Name of the endpoint within the API
                parameters: Dictionary of parameters to pass to the endpoint
                ctx: Optional context for logging
            
            Returns:
                API response data and metadata
            
            Example:
                # Call OpenWeatherMap API
                result = await call_api(
                    api_name="OpenWeatherMap",
                    endpoint_name="get_weather",
                    parameters={"q": "London", "units": "metric"}
                )
                
                # Call GitHub API
                result = await call_api(
                    api_name="GitHub",
                    endpoint_name="get_user",
                    parameters={"username": "octocat"}
                )
            """
            if parameters is None:
                parameters = {}
            
            # Validate API exists
            if api_name not in self.apis:
                available_apis = list(self.apis.keys())
                error_msg = f"API '{api_name}' not found. Available APIs: {', '.join(available_apis)}"
                if ctx:
                    await ctx.error(error_msg)
                raise ValueError(error_msg)
            
            # Find the endpoint
            api_config = self.apis[api_name]
            endpoint = None
            for ep in api_config.endpoints:
                if ep.name == endpoint_name:
                    endpoint = ep
                    break
            
            if not endpoint:
                available_endpoints = [ep.name for ep in api_config.endpoints]
                error_msg = f"Endpoint '{endpoint_name}' not found in API '{api_name}'. Available endpoints: {', '.join(available_endpoints)}"
                if ctx:
                    await ctx.error(error_msg)
                raise ValueError(error_msg)
            
            if ctx:
                await ctx.info(f"Calling {api_name}.{endpoint_name} with parameters: {parameters}")
            
            try:
                # Call the API using existing method
                response_data = await self._execute_api_call(
                    api_name=api_name,
                    endpoint_name=endpoint_name,
                    params=parameters,
                    ctx=ctx
                )
                
                # Return structured response with metadata
                result = {
                    "success": True,
                    "api_name": api_name,
                    "endpoint_name": endpoint_name,
                    "endpoint_info": {
                        "method": endpoint.method,
                        "path": endpoint.path,
                        "description": endpoint.description
                    },
                    "parameters_used": parameters,
                    "data": response_data
                }
                
                if ctx:
                    await ctx.info(f"Successfully called {api_name}.{endpoint_name}")
                
                return result
                
            except Exception as e:
                error_result = {
                    "success": False,
                    "api_name": api_name,
                    "endpoint_name": endpoint_name,
                    "parameters_used": parameters,
                    "error": str(e),
                    "error_type": type(e).__name__
                }
                
                if ctx:
                    await ctx.error(f"Failed to call {api_name}.{endpoint_name}: {str(e)}")
                
                return error_result
        
        @self.mcp.tool()
        async def get_api_schema(api_name: str, endpoint_name: str = None, ctx: Optional[Context] = None) -> Dict[str, Any]:
            """
            Get the schema/documentation for an API or specific endpoint.
            
            This tool helps understand what parameters are available for API calls
            and their requirements before making actual calls.
            
            Args:
                api_name: Name of the registered API
                endpoint_name: Optional specific endpoint name. If not provided, returns all endpoints
                ctx: Optional context for logging
            
            Returns:
                Schema information for the API or endpoint
            """
            if api_name not in self.apis:
                available_apis = list(self.apis.keys())
                error_msg = f"API '{api_name}' not found. Available APIs: {', '.join(available_apis)}"
                if ctx:
                    await ctx.error(error_msg)
                raise ValueError(error_msg)
            
            api_config = self.apis[api_name]
            
            if endpoint_name:
                # Return specific endpoint schema
                endpoint = None
                for ep in api_config.endpoints:
                    if ep.name == endpoint_name:
                        endpoint = ep
                        break
                
                if not endpoint:
                    available_endpoints = [ep.name for ep in api_config.endpoints]
                    error_msg = f"Endpoint '{endpoint_name}' not found in API '{api_name}'. Available endpoints: {', '.join(available_endpoints)}"
                    if ctx:
                        await ctx.error(error_msg)
                    raise ValueError(error_msg)
                
                return {
                    "api_name": api_name,
                    "endpoint_name": endpoint_name,
                    "method": endpoint.method,
                    "path": endpoint.path,
                    "description": endpoint.description,
                    "parameters": [
                        {
                            "name": param.name,
                            "type": param.type,
                            "location": param.location,
                            "required": param.required,
                            "description": param.description,
                            "default": param.default,
                            "enum": param.enum
                        }
                        for param in endpoint.params
                    ],
                    "headers": endpoint.headers,
                    "timeout": endpoint.timeout
                }
            else:
                # Return all endpoints schema
                return {
                    "api_name": api_name,
                    "base_url": api_config.base_url,
                    "description": api_config.description,
                    "auth_type": api_config.auth.type if api_config.auth else "none",
                    "global_headers": api_config.headers,
                    "endpoints": [
                        {
                            "name": ep.name,
                            "method": ep.method,
                            "path": ep.path,
                            "description": ep.description,
                            "parameters": [
                                {
                                    "name": param.name,
                                    "type": param.type,
                                    "location": param.location,
                                    "required": param.required,
                                    "description": param.description,
                                    "default": param.default,
                                    "enum": param.enum
                                }
                                for param in ep.params
                            ]
                        }
                        for ep in api_config.endpoints
                    ]
                }
    
    async def _create_http_client(self, api_config: APIConfig) -> httpx.AsyncClient:
        """Create an HTTP client with authentication configured."""
        headers = {}
        auth = None
        
        # Add global headers
        if api_config.headers:
            headers.update(api_config.headers)
        
        # Configure authentication
        if api_config.auth:
            auth_config = api_config.auth
            
            if auth_config.type == "bearer" and auth_config.bearer_token:
                headers["Authorization"] = f"Bearer {auth_config.bearer_token}"
            
            elif auth_config.type == "api_key":
                if auth_config.api_key_header and auth_config.api_key:
                    headers[auth_config.api_key_header] = auth_config.api_key
            
            elif auth_config.type == "basic" and auth_config.username and auth_config.password:
                auth = httpx.BasicAuth(auth_config.username, auth_config.password)
            
            elif auth_config.type == "custom" and auth_config.custom_headers:
                headers.update(auth_config.custom_headers)
        
        # Create client
        client = httpx.AsyncClient(
            base_url=api_config.base_url,
            headers=headers,
            auth=auth,
            timeout=30.0,
            follow_redirects=True
        )
        
        return client
    
    def _generate_param_collection_code(self, endpoint: APIEndpoint) -> str:
        """Generate code to collect parameters explicitly."""
        lines = []
        for param in endpoint.params:
            lines.append(f"    call_params['{param.name}'] = {param.name}")
        return "\n".join(lines)
    
    async def _create_endpoint_tool(self, api_config: APIConfig, endpoint: APIEndpoint, tool_name: str):
        """Create an MCP tool for a specific API endpoint using closure approach."""
        
        # Build parameter signature
        sig_parts = []
        param_annotations = {}
        
        for param in endpoint.params:
            # Determine Python type
            param_type = str
            if param.type == "integer":
                param_type = int
            elif param.type == "number":
                param_type = float
            elif param.type == "boolean":
                param_type = bool
            elif param.type == "array":
                param_type = List[Any]
            elif param.type == "object":
                param_type = Dict[str, Any]
            
            # Build parameter with default if not required
            if param.required:
                sig_parts.append(param.name)
            else:
                default_val = param.default if param.default is not None else None
                sig_parts.append(f"{param.name}={repr(default_val)}")
            
            param_annotations[param.name] = param_type
        
        # Add context parameter
        sig_parts.append("ctx: Optional[Context] = None")
        param_annotations["ctx"] = Optional[Context]
        param_annotations["return"] = Any
        
        # Create the closure-based tool function
        def create_tool_function():
            # Capture the current values
            api_name = api_config.name
            endpoint_name = endpoint.name
            
            async def api_tool_func(*args, **kwargs):
                # Map positional args to parameter names
                param_names = [p.name for p in endpoint.params]
                call_params = {}
                
                # Handle positional arguments
                for i, arg in enumerate(args):
                    if i < len(param_names):
                        call_params[param_names[i]] = arg
                
                # Handle keyword arguments
                ctx = kwargs.pop('ctx', None)
                call_params.update(kwargs)
                
                return await self._execute_api_call(
                    api_name=api_name,
                    endpoint_name=endpoint_name,
                    params=call_params,
                    ctx=ctx
                )
            
            # Set function metadata
            api_tool_func.__name__ = tool_name
            api_tool_func.__doc__ = f"""
{endpoint.description}

Generated tool for {api_config.name} API endpoint: {endpoint.method} {endpoint.path}

Parameters:
{self._generate_param_docs(endpoint)}
"""
            api_tool_func.__annotations__ = param_annotations
            
            return api_tool_func
        
        # Create and register the tool
        tool_function = create_tool_function()
        self.mcp.add_tool(tool_function)
    
    def _generate_param_docs(self, endpoint: APIEndpoint) -> str:
        """Generate parameter documentation for the tool."""
        docs = []
        for param in endpoint.params:
            required_str = "required" if param.required else "optional"
            default_str = f" (default: {param.default})" if param.default is not None else ""
            desc = param.description or ""
            docs.append(f"- {param.name} ({param.type}, {required_str}){default_str}: {desc}")
        return "\n".join(docs)
    
    async def _execute_api_call(self, api_name: str, endpoint_name: str, params: Dict[str, Any], ctx: Optional[Context] = None) -> Any:
        """Execute an API call with the given parameters."""
        
        # Get API config and endpoint
        api_config = self.apis.get(api_name)
        if not api_config:
            raise ValueError(f"API '{api_name}' not found")
        
        endpoint = None
        for ep in api_config.endpoints:
            if ep.name == endpoint_name:
                endpoint = ep
                break
        
        if not endpoint:
            raise ValueError(f"Endpoint '{endpoint_name}' not found in API '{api_name}'")
        
        # Get HTTP client
        client = self.http_clients.get(api_name)
        if not client:
            raise ValueError(f"No HTTP client found for API '{api_name}'")
        
        # Build request
        url_path = endpoint.path
        query_params = {}
        headers = {}
        json_body = None
        
        # Add endpoint-specific headers
        if endpoint.headers:
            headers.update(endpoint.headers)
        
        # Process parameters
        for param in endpoint.params:
            value = params.get(param.name)
            
            # Use default value if not provided
            if value is None and param.default is not None:
                value = param.default
            
            # Check required parameters
            if value is None and param.required:
                raise ValueError(f"Required parameter '{param.name}' not provided")
            
            # Skip None values for optional parameters
            if value is None:
                continue
            
            if param.location == "path":
                # Replace path parameter
                url_path = url_path.replace(f"{{{param.name}}}", quote(str(value)))
            elif param.location == "query":
                query_params[param.name] = value
            elif param.location == "header":
                headers[param.name] = str(value)
            elif param.location == "body":
                if json_body is None:
                    json_body = {}
                json_body[param.name] = value
        
        # Handle API key in query params
        if api_config.auth and api_config.auth.type == "api_key" and api_config.auth.api_key_param:
            query_params[api_config.auth.api_key_param] = api_config.auth.api_key
        
        # Make request
        try:
            if ctx:
                await ctx.info(f"Calling {endpoint.method} {url_path}")
            
            response = await client.request(
                method=endpoint.method,
                url=url_path,
                params=query_params if query_params else None,
                headers=headers if headers else None,
                json=json_body,
                timeout=endpoint.timeout
            )
            
            response.raise_for_status()
            
            # Parse response
            content_type = response.headers.get("content-type", "")
            if content_type.startswith("application/json"):
                return response.json()
            else:
                return response.text
                
        except httpx.HTTPStatusError as e:
            error_msg = f"HTTP {e.response.status_code}: {e.response.text}"
            if ctx:
                await ctx.error(error_msg)
            raise ValueError(error_msg)
        except Exception as e:
            if ctx:
                await ctx.error(f"Request failed: {str(e)}")
            raise
    
    def run(self, **kwargs):
        """Run the MCP server."""
        return self.mcp.run(**kwargs)