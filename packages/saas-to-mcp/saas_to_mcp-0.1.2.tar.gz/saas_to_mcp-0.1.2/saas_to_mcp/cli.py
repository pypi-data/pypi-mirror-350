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
        if config_path.exists():
            with open(config_path, 'r') as f:
                api_config = json.load(f)
            
            # Register API from config file
            # This would need to be done through the MCP protocol
            # For now, we'll just start the server
            click.echo(f"Loaded configuration from {config}")
    
    # Run server with appropriate transport
    if transport == "stdio":
        click.echo(f"Starting {name} server on stdio transport...")
        server.run()
    else:
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


if __name__ == "__main__":
    main()
