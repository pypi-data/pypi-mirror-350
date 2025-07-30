#!/usr/bin/env python3
"""
SaasToMCP - A FastMCP server that dynamically creates MCP servers from web API configurations.

This server allows you to define web APIs (REST, GraphQL, etc.) and automatically
converts them into MCP tools that can be used by AI assistants.
"""

import json
import asyncio
from typing import Dict, Any, Optional, List, Union
from urllib.parse import urljoin, quote
import httpx
from fastmcp import FastMCP, Context
from pydantic import BaseModel, Field, ConfigDict


class AuthConfig(BaseModel):
    """Authentication configuration for API requests."""
    model_config = ConfigDict(extra='allow')
    
    type: str = Field(..., description="Auth type: bearer, api_key, basic, oauth2, custom")
    bearer_token: Optional[str] = Field(None, description="Bearer token for bearer auth")
    api_key: Optional[str] = Field(None, description="API key value")
    api_key_header: Optional[str] = Field("X-API-Key", description="Header name for API key")
    api_key_param: Optional[str] = Field(None, description="Query parameter name for API key")
    username: Optional[str] = Field(None, description="Username for basic auth")
    password: Optional[str] = Field(None, description="Password for basic auth")
    oauth2_token_url: Optional[str] = Field(None, description="OAuth2 token endpoint")
    oauth2_client_id: Optional[str] = Field(None, description="OAuth2 client ID")
    oauth2_client_secret: Optional[str] = Field(None, description="OAuth2 client secret")
    oauth2_scope: Optional[str] = Field(None, description="OAuth2 scope")
    custom_headers: Optional[Dict[str, str]] = Field(None, description="Custom auth headers")


class RequestParam(BaseModel):
    """Parameter definition for API requests."""
    name: str = Field(..., description="Parameter name")
    type: str = Field("string", description="Parameter type: string, integer, number, boolean, array, object")
    location: str = Field("query", description="Parameter location: query, path, header, body")
    required: bool = Field(False, description="Whether parameter is required")
    description: Optional[str] = Field(None, description="Parameter description")
    default: Optional[Any] = Field(None, description="Default value")
    enum: Optional[List[Any]] = Field(None, description="Allowed values")


class APIEndpoint(BaseModel):
    """Configuration for a single API endpoint."""
    name: str = Field(..., description="Tool name for this endpoint")
    description: str = Field(..., description="Description of what this endpoint does")
    method: str = Field("GET", description="HTTP method: GET, POST, PUT, DELETE, PATCH, etc.")
    path: str = Field(..., description="API path, can include {param} placeholders")
    params: List[RequestParam] = Field(default_factory=list, description="Request parameters")
    request_body_schema: Optional[Dict[str, Any]] = Field(None, description="JSON Schema for request body")
    response_schema: Optional[Dict[str, Any]] = Field(None, description="JSON Schema for response")
    headers: Optional[Dict[str, str]] = Field(None, description="Additional headers for this endpoint")
    timeout: Optional[float] = Field(30.0, description="Request timeout in seconds")


class APIConfig(BaseModel):
    """Configuration for an entire API."""
    name: str = Field(..., description="API name")
    base_url: str = Field(..., description="Base URL for the API")
    description: Optional[str] = Field(None, description="API description")
    auth: Optional[AuthConfig] = Field(None, description="Authentication configuration")
    headers: Optional[Dict[str, str]] = Field(None, description="Global headers for all requests")
    endpoints: List[APIEndpoint] = Field(..., description="List of API endpoints")


class SaasToMCP:
    """Main server that creates MCP tools from API configurations."""
    
    def __init__(self):
        self.mcp = FastMCP("SaasToMCP")
        self.apis: Dict[str, APIConfig] = {}
        self.http_clients: Dict[str, httpx.AsyncClient] = {}
        self._setup_tools()
    
    def _setup_tools(self):
        """Set up the core tools for managing APIs."""
        
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
                    await self._create_endpoint_tool(api_config, endpoint, tool_name)
                    created_tools.append(tool_name)
                
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
                            "description": ep.description
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
    
    async def _create_endpoint_tool(self, api_config: APIConfig, endpoint: APIEndpoint, tool_name: str):
        """Create an MCP tool for a specific API endpoint."""
        
        # Build parameter schema for the tool
        tool_params = {}
        required_params = []
        
        for param in endpoint.params:
            param_schema = {"type": param.type}
            if param.description:
                param_schema["description"] = param.description
            if param.enum:
                param_schema["enum"] = param.enum
            if param.default is not None:
                param_schema["default"] = param.default
            
            tool_params[param.name] = param_schema
            if param.required:
                required_params.append(param.name)
        
        # Create the tool function
        async def api_tool_function(**kwargs) -> Any:
            """Dynamic API tool function."""
            ctx = kwargs.get('ctx')
            if ctx:
                kwargs.pop('ctx')
            
            # Get HTTP client
            client = self.http_clients.get(api_config.name)
            if not client:
                raise ValueError(f"No HTTP client found for API '{api_config.name}'")
            
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
                value = kwargs.get(param.name)
                if value is None and param.required:
                    raise ValueError(f"Required parameter '{param.name}' not provided")
                
                if value is not None:
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
                if response.headers.get("content-type", "").startswith("application/json"):
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
        
        # Set function metadata
        api_tool_function.__name__ = tool_name
        api_tool_function.__doc__ = endpoint.description
        
        # Add Context parameter to the function signature if needed
        import inspect
        sig = inspect.signature(api_tool_function)
        params = list(sig.parameters.values())
        
        # Add regular parameters
        for param_name, param_schema in tool_params.items():
            param_type = str
            if param_schema["type"] == "integer":
                param_type = int
            elif param_schema["type"] == "number":
                param_type = float
            elif param_schema["type"] == "boolean":
                param_type = bool
            elif param_schema["type"] == "array":
                param_type = List[Any]
            elif param_schema["type"] == "object":
                param_type = Dict[str, Any]
            
            default = param_schema.get("default", inspect.Parameter.empty)
            params.append(
                inspect.Parameter(
                    param_name,
                    inspect.Parameter.KEYWORD_ONLY,
                    default=default,
                    annotation=param_type
                )
            )
        
        # Add Context parameter
        params.append(
            inspect.Parameter(
                "ctx",
                inspect.Parameter.KEYWORD_ONLY,
                default=None,
                annotation=Optional[Context]
            )
        )
        
        api_tool_function.__signature__ = sig.replace(parameters=params)
        
        # Register the tool
        self.mcp.add_tool(api_tool_function)
    
    def run(self):
        """Run the MCP server."""
        return self.mcp.run()


def main():
    server = SaasToMCP()
    server.run()


if __name__ == "__main__":
    main()