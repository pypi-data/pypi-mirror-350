"""
Command-line interface for SaasToMCP.

This module provides the CLI entry point for running SaasToMCP servers.
"""

import sys
import json
import asyncio
from pathlib import Path
from typing import Optional
import click
from .server import SaasToMCP


@click.group()
@click.version_option()
def main():
    """SaasToMCP - Convert any SaaS API into an MCP server."""
    pass


@main.command()
@click.option("--name", default="SaasToMCP", help="Server name")
@click.option("--config", type=click.Path(exists=True), help="API configuration file (JSON)")
@click.option("--transport", default="stdio", type=click.Choice(["stdio", "sse"]), help="Transport type")
@click.option("--host", default="127.0.0.1", help="Host for SSE transport")
@click.option("--port", default=8000, type=int, help="Port for SSE transport")
@click.option("--path", default="/mcp", help="Path for SSE transport")
def run(name: str, config: Optional[str], transport: str, host: str, port: int, path: str):
    """Run the SaasToMCP server."""
    
    # Create server
    server = SaasToMCP(name=name)
    
    # Load configuration if provided
    if config:
        config_path = Path(config)
        try:
            with open(config_path, 'r') as f:
                api_config = json.load(f)
            
            # Register the API
            async def register_config():
                try:
                    # Create a mock context for the registration
                    class MockContext:
                        def __init__(self):
                            pass
                    
                    ctx = MockContext()
                    result = await server.mcp._tools["register_api"](config=api_config, ctx=ctx)
                    click.echo(f"✅ {result}")
                except Exception as e:
                    click.echo(f"❌ Failed to load config: {e}")
                    sys.exit(1)
            
            # Register config before starting server
            asyncio.run(register_config())
            
        except Exception as e:
            click.echo(f"❌ Failed to load configuration from {config_path}: {e}")
            sys.exit(1)
    
    # Run server with specified transport
    try:
        if transport == "stdio":
            click.echo(f"🚀 Starting {name} server with stdio transport...")
            server.run()
        else:  # sse
            click.echo(f"🚀 Starting {name} server with SSE transport at http://{host}:{port}{path}")
            server.run(transport="sse", host=host, port=port, path=path)
    except KeyboardInterrupt:
        click.echo("\n👋 Shutting down server...")
    except Exception as e:
        click.echo(f"❌ Server error: {e}")
        sys.exit(1)


@main.command()
@click.argument("config_file", type=click.Path(exists=True))
def validate(config_file: str):
    """Validate an API configuration file."""
    
    config_path = Path(config_file)
    
    try:
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        
        # Try to parse as APIConfig
        from .models import APIConfig
        api_config = APIConfig(**config_data)
        
        click.echo(f"✅ Configuration is valid!")
        click.echo(f"API Name: {api_config.name}")
        click.echo(f"Base URL: {api_config.base_url}")
        click.echo(f"Endpoints: {len(api_config.endpoints)}")
        
        for endpoint in api_config.endpoints:
            click.echo(f"  - {endpoint.method} {endpoint.path} ({endpoint.name})")
        
    except json.JSONDecodeError as e:
        click.echo(f"❌ Invalid JSON: {e}")
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Configuration error: {e}")
        sys.exit(1)


@main.command()
def examples():
    """Show example API configurations."""
    
    click.echo("📋 Example API Configurations:\n")
    
    # JSONPlaceholder example
    jsonplaceholder_example = {
        "name": "jsonplaceholder",
        "base_url": "https://jsonplaceholder.typicode.com",
        "description": "Free fake API for testing",
        "endpoints": [
            {
                "name": "list_posts",
                "description": "Get all posts",
                "method": "GET",
                "path": "/posts",
                "params": [
                    {
                        "name": "_limit",
                        "type": "integer",
                        "location": "query",
                        "required": False,
                        "description": "Limit number of results"
                    }
                ]
            }
        ]
    }
    
    click.echo("1. JSONPlaceholder API (No Auth):")
    click.echo(json.dumps(jsonplaceholder_example, indent=2))
    
    # Weather API example
    weather_example = {
        "name": "weather",
        "base_url": "https://api.openweathermap.org/data/2.5",
        "description": "OpenWeatherMap API",
        "auth": {
            "type": "api_key",
            "api_key": "YOUR_API_KEY",
            "api_key_param": "appid"
        },
        "endpoints": [
            {
                "name": "get_weather",
                "description": "Get current weather",
                "method": "GET",
                "path": "/weather",
                "params": [
                    {
                        "name": "q",
                        "type": "string",
                        "location": "query",
                        "required": True,
                        "description": "City name"
                    }
                ]
            }
        ]
    }
    
    click.echo("\n2. Weather API (API Key Auth):")
    click.echo(json.dumps(weather_example, indent=2))
    
    # GitHub API example
    github_example = {
        "name": "github",
        "base_url": "https://api.github.com",
        "description": "GitHub REST API",
        "auth": {
            "type": "bearer",
            "bearer_token": "ghp_YOUR_TOKEN"
        },
        "endpoints": [
            {
                "name": "get_user",
                "description": "Get user info",
                "method": "GET",
                "path": "/users/{username}",
                "params": [
                    {
                        "name": "username",
                        "type": "string",
                        "location": "path",
                        "required": True,
                        "description": "GitHub username"
                    }
                ]
            }
        ]
    }
    
    click.echo("\n3. GitHub API (Bearer Token Auth):")
    click.echo(json.dumps(github_example, indent=2))


if __name__ == "__main__":
    main()
