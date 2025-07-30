"""
Command-line interface for SaasToMCP.
"""

import json
import click
from pathlib import Path
from typing import Optional
from .server import SaasToMCP


@click.group()
def main():
    """SaasToMCP - Convert any SaaS API into an MCP server."""
    pass


@main.command()
@click.option("--name", default="SaasToMCP", help="Server name")
@click.option("--config", type=click.Path(exists=True), help="API configuration file (JSON)")
@click.option("--transport", default="stdio", type=click.Choice(["stdio", "sse", "streamable-http"]), help="Transport type")
@click.option("--host", default="127.0.0.1", help="Host for HTTP transports")
@click.option("--port", default=8000, type=int, help="Port for HTTP transports")
@click.option("--path", default="/mcp", help="Path for HTTP transports")
def run(name: str, config: Optional[str], transport: str, host: str, port: int, path: str):
    """Run the SaasToMCP server."""
    
    # Create server
    server = SaasToMCP(name=name)
    
    # Load configuration if provided
    if config:
        config_path = Path(config)
        if config_path.exists():
            with open(config_path, 'r') as f:
                api_config = json.load(f)
            
            # Register API from config file
            # This would need to be done through the MCP protocol
            # For now, we'll just start the server
            click.echo(f"Loaded configuration from {config}")
    
    # Run server with appropriate transport
    if transport == "stdio":
        click.echo(f"Starting {name} server on STDIO transport...")
        server.run()
    elif transport == "streamable-http":
        click.echo(f"Starting {name} server on Streamable HTTP transport at http://{host}:{port}{path}")
        server.run(transport="streamable-http", host=host, port=port, path=path)
    else:  # sse
        click.echo(f"Starting {name} server on SSE transport at http://{host}:{port}{path}")
        server.run(transport="sse", host=host, port=port, path=path)


@main.command()
def examples():
    """Show example API configurations."""
    
    # OpenWeatherMap Example
    weather_example = {
        "name": "OpenWeatherMap",
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
                "description": "Get current weather for a city",
                "method": "GET",
                "path": "/weather",
                "params": [
                    {
                        "name": "q",
                        "type": "string",
                        "location": "query",
                        "required": True,
                        "description": "City name"
                    },
                    {
                        "name": "units",
                        "type": "string",
                        "location": "query",
                        "default": "metric",
                        "enum": ["standard", "metric", "imperial"],
                        "description": "Temperature units"
                    }
                ]
            }
        ]
    }
    
    click.echo("Example API Configurations:\n")
    click.echo("1. OpenWeatherMap API (API Key in Query):")
    click.echo(json.dumps(weather_example, indent=2))
    
    # JSONPlaceholder Example
    jsonplaceholder_example = {
        "name": "JSONPlaceholder",
        "base_url": "https://jsonplaceholder.typicode.com",
        "description": "Fake REST API for testing",
        "endpoints": [
            {
                "name": "get_post",
                "description": "Get a post by ID",
                "method": "GET",
                "path": "/posts/{id}",
                "params": [
                    {
                        "name": "id",
                        "type": "integer",
                        "location": "path",
                        "required": True,
                        "description": "Post ID"
                    }
                ]
            },
            {
                "name": "create_post",
                "description": "Create a new post",
                "method": "POST",
                "path": "/posts",
                "params": [
                    {
                        "name": "title",
                        "type": "string",
                        "location": "body",
                        "required": True,
                        "description": "Post title"
                    },
                    {
                        "name": "body",
                        "type": "string",
                        "location": "body",
                        "required": True,
                        "description": "Post body"
                    },
                    {
                        "name": "userId",
                        "type": "integer",
                        "location": "body",
                        "required": True,
                        "description": "User ID"
                    }
                ]
            }
        ]
    }
    
    click.echo("\n2. JSONPlaceholder API (No Auth):")
    click.echo(json.dumps(jsonplaceholder_example, indent=2))
    
    # GitHub API Example
    github_example = {
        "name": "GitHub",
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


@main.command()
def transports():
    """Show information about available transport types."""
    
    click.echo("Available Transport Types:\n")
    
    click.echo("1. STDIO (Default)")
    click.echo("   Usage: saas-to-mcp run")
    click.echo("   Best for: Local tools, CLI usage")
    click.echo("   Characteristics: Direct process communication, lowest latency\n")
    
    click.echo("2. SSE (Server-Sent Events)")
    click.echo("   Usage: saas-to-mcp run --transport sse --host 127.0.0.1 --port 8000")
    click.echo("   Best for: Legacy MCP clients")
    click.echo("   Characteristics: HTTP-based, one-way streaming")
    click.echo("   Note: Deprecated in favor of Streamable HTTP\n")
    
    click.echo("3. Streamable HTTP (Recommended)")
    click.echo("   Usage: saas-to-mcp run --transport streamable-http --host 127.0.0.1 --port 8000")
    click.echo("   Best for: Modern web deployments, cloud environments")
    click.echo("   Characteristics: Full HTTP communication, bidirectional streaming")
    click.echo("   Endpoint: http://host:port/mcp\n")
    
    click.echo("Examples:")
    click.echo("  # Local usage")
    click.echo("  saas-to-mcp run")
    click.echo("")
    click.echo("  # Modern HTTP transport")
    click.echo("  saas-to-mcp run --transport streamable-http --port 8000")
    click.echo("")
    click.echo("  # Legacy SSE transport")
    click.echo("  saas-to-mcp run --transport sse --port 8001")


if __name__ == "__main__":
    main()