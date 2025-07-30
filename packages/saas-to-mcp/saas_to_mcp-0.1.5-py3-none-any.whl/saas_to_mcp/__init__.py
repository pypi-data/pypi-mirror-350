"""
SaasToMCP - Convert any SaaS API into an MCP server.

This package provides a framework for dynamically creating MCP (Model Context Protocol)
servers from web API configurations, making it easy to integrate REST APIs, GraphQL
endpoints, and other web services with AI assistants.
"""

__version__ = "0.1.0"
__author__ = "SaasToMCP Contributors"

from .server import SaasToMCP
from .models import APIConfig, APIEndpoint, AuthConfig, RequestParam

__all__ = [
    "SaasToMCP",
    "APIConfig", 
    "APIEndpoint",
    "AuthConfig",
    "RequestParam"
]
