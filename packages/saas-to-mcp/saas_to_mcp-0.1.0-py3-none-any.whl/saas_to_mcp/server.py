"""
Main SaasToMCP server implementation.

This module provides the core server functionality for converting web APIs
into MCP (Model Context Protocol) tools.
"""

import json
import asyncio
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
                
                # Log the endpoints that would be created
                created_tools = []
                for endpoint in api_config.endpoints:
                    tool_name = f"{api_config.name}_{endpoint.name}"
                    created_tools.append(tool_name)
                
                print(f"Registered API '{api_config.name}' with {len(created_tools)} endpoints")
                return f"Successfully registered API '{api_config.name}' with endpoints: {', '.join(created_tools)}. Note: Individual endpoint tools need to be created dynamically."
                
            except Exception as e:
                print(f"Failed to register API: {str(e)}")
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
        async def call_api_endpoint(
            api_name: str, 
            endpoint_name: str, 
            parameters: Optional[Dict[str, Any]] = None,
            ctx: Context = None
        ) -> Any:
            """
            Call a specific API endpoint with the given parameters.
            
            Args:
                api_name: Name of the registered API
                endpoint_name: Name of the endpoint to call
                parameters: Dictionary of parameters to pass to the endpoint
            
            Returns:
                API response data
            """
            if api_name not in self.apis:
                raise ValueError(f"API '{api_name}' not found. Available APIs: {list(self.apis.keys())}")
            
            api_config = self.apis[api_name]
            endpoint = None
            
            # Find the endpoint
            for ep in api_config.endpoints:
                if ep.name == endpoint_name:
                    endpoint = ep
                    break
            
            if not endpoint:
                available_endpoints = [ep.name for ep in api_config.endpoints]
                raise ValueError(f"Endpoint '{endpoint_name}' not found in API '{api_name}'. Available endpoints: {available_endpoints}")
            
            # Get HTTP client
            client = self.http_clients.get(api_name)
            if not client:
                raise ValueError(f"No HTTP client found for API '{api_name}'")
            
            # Build request
            return await self._make_api_request(api_config, endpoint, parameters or {}, client, ctx)
        
        @self.mcp.tool()
        async def unregister_api(api_name: str, ctx: Context) -> str:
            """
            Unregister an API and clean up its resources.
            
            Args:
                api_name: Name of the API to unregister
            
            Returns:
                Success message
            """
            if api_name not in self.apis:
                raise ValueError(f"API '{api_name}' not found")
            
            # Close HTTP client
            if api_name in self.http_clients:
                await self.http_clients[api_name].aclose()
                del self.http_clients[api_name]
            
            # Remove API config
            del self.apis[api_name]
            
            print(f"Unregistered API '{api_name}'")
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
    
    async def _make_api_request(
        self, 
        api_config: APIConfig, 
        endpoint: APIEndpoint, 
        parameters: Dict[str, Any],
        client: httpx.AsyncClient,
        ctx: Optional[Context] = None
    ) -> Any:
        """Make an API request to the specified endpoint."""
        
        # Build request components
        url_path = endpoint.path
        query_params = {}
        headers = {}
        json_body = None
        
        # Add endpoint-specific headers
        if endpoint.headers:
            headers.update(endpoint.headers)
        
        # Process parameters
        for param in endpoint.params:
            value = parameters.get(param.name)
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
                print(f"Calling {endpoint.method} {url_path}")
            
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
                print(f"API Error: {error_msg}")
            raise ValueError(error_msg)
        except Exception as e:
            if ctx:
                print(f"Request failed: {str(e)}")
            raise
    
    async def cleanup(self):
        """Clean up HTTP clients."""
        for client in self.http_clients.values():
            await client.aclose()
        self.http_clients.clear()
    
    def run(self, **kwargs):
        """Run the MCP server."""
        try:
            return self.mcp.run(**kwargs)
        finally:
            # Cleanup on shutdown
            asyncio.create_task(self.cleanup())


def create_server(name: str = "SaasToMCP") -> SaasToMCP:
    """Create a new SaasToMCP server instance."""
    return SaasToMCP(name=name)
