"""
Data models for SaasToMCP.
"""

from typing import Dict, Any, Optional, List
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
