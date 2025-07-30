# SaasToMCP

A FastMCP server that dynamically creates MCP (Model Context Protocol) servers from web API configurations. This allows you to easily integrate any REST API, GraphQL endpoint, or web service into an MCP-compatible tool that can be used by AI assistants like Claude.

## Features

- 🚀 **Dynamic API Registration**: Register any web API at runtime
- 🔐 **Multiple Authentication Methods**: Bearer tokens, API keys, Basic auth, OAuth2, and custom headers
- 🛠️ **All HTTP Methods**: Support for GET, POST, PUT, DELETE, PATCH, and more
- 📝 **Flexible Parameters**: Query params, path params, headers, and request bodies
- 🔄 **Automatic Tool Generation**: Each API endpoint becomes an MCP tool
- 🧪 **Built-in Testing**: Test API connections before using them
- 📊 **Response Handling**: Automatic JSON parsing with fallback to text

## Installation

```bash
# Clone or download this repository
cd ~/Desktop/SaasToMCP

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Starting the Server

```bash
python saas_to_mcp.py
```

Or use with the MCP CLI:

```bash
mcp install saas_to_mcp.py
```

### Core Tools

The server provides these built-in tools:

1. **register_api** - Register a new API and create tools for its endpoints
2. **list_apis** - List all registered APIs and their endpoints
3. **unregister_api** - Remove an API and its tools
4. **test_api_connection** - Test connectivity to a registered API

### API Configuration Format

```json
{
  "name": "my_api",
  "base_url": "https://api.example.com",
  "description": "Example API integration",
  "auth": {
    "type": "bearer",
    "bearer_token": "your-token-here"
  },
  "headers": {
    "Accept": "application/json"
  },
  "endpoints": [
    {
      "name": "list_users",
      "description": "Get all users",
      "method": "GET",
      "path": "/users",
      "params": [
        {
          "name": "limit",
          "type": "integer",
          "location": "query",
          "required": false,
          "default": 10,
          "description": "Number of users to return"
        }
      ]
    }
  ]
}
```

## Examples

### Example 1: OpenWeatherMap API

```json
{
  "name": "weather",
  "base_url": "https://api.openweathermap.org/data/2.5",
  "description": "OpenWeatherMap API",
  "auth": {
    "type": "api_key",
    "api_key": "your-api-key",
    "api_key_param": "appid"
  },
  "endpoints": [
    {
      "name": "get_current_weather",
      "description": "Get current weather for a city",
      "method": "GET",
      "path": "/weather",
      "params": [
        {
          "name": "q",
          "type": "string",
          "location": "query",
          "required": true,
          "description": "City name"
        },
        {
          "name": "units",
          "type": "string",
          "location": "query",
          "required": false,
          "default": "metric",
          "enum": ["metric", "imperial", "kelvin"]
        }
      ]
    }
  ]
}
```

### Example 2: GitHub API

```json
{
  "name": "github",
  "base_url": "https://api.github.com",
  "description": "GitHub REST API",
  "auth": {
    "type": "bearer",
    "bearer_token": "ghp_your_token_here"
  },
  "headers": {
    "Accept": "application/vnd.github.v3+json"
  },
  "endpoints": [
    {
      "name": "get_user",
      "description": "Get a GitHub user's information",
      "method": "GET",
      "path": "/users/{username}",
      "params": [
        {
          "name": "username",
          "type": "string",
          "location": "path",
          "required": true,
          "description": "GitHub username"
        }
      ]
    },
    {
      "name": "create_issue",
      "description": "Create a new issue in a repository",
      "method": "POST",
      "path": "/repos/{owner}/{repo}/issues",
      "params": [
        {
          "name": "owner",
          "type": "string",
          "location": "path",
          "required": true,
          "description": "Repository owner"
        },
        {
          "name": "repo",
          "type": "string",
          "location": "path",
          "required": true,
          "description": "Repository name"
        },
        {
          "name": "title",
          "type": "string",
          "location": "body",
          "required": true,
          "description": "Issue title"
        },
        {
          "name": "body",
          "type": "string",
          "location": "body",
          "required": false,
          "description": "Issue description"
        },
        {
          "name": "labels",
          "type": "array",
          "location": "body",
          "required": false,
          "description": "Array of label names"
        }
      ]
    }
  ]
}
```

### Example 3: Stripe API

```json
{
  "name": "stripe",
  "base_url": "https://api.stripe.com/v1",
  "description": "Stripe Payment API",
  "auth": {
    "type": "basic",
    "username": "sk_test_your_key_here",
    "password": ""
  },
  "endpoints": [
    {
      "name": "list_customers",
      "description": "List all customers",
      "method": "GET",
      "path": "/customers",
      "params": [
        {
          "name": "limit",
          "type": "integer",
          "location": "query",
          "required": false,
          "default": 10
        },
        {
          "name": "starting_after",
          "type": "string",
          "location": "query",
          "required": false,
          "description": "Cursor for pagination"
        }
      ]
    },
    {
      "name": "create_customer",
      "description": "Create a new customer",
      "method": "POST",
      "path": "/customers",
      "headers": {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      "params": [
        {
          "name": "email",
          "type": "string",
          "location": "body",
          "required": true,
          "description": "Customer email"
        },
        {
          "name": "name",
          "type": "string",
          "location": "body",
          "required": false,
          "description": "Customer name"
        }
      ]
    }
  ]
}
```

## Authentication Types

### Bearer Token
```json
{
  "auth": {
    "type": "bearer",
    "bearer_token": "your-token-here"
  }
}
```

### API Key (Header)
```json
{
  "auth": {
    "type": "api_key",
    "api_key": "your-key-here",
    "api_key_header": "X-API-Key"
  }
}
```

### API Key (Query Parameter)
```json
{
  "auth": {
    "type": "api_key",
    "api_key": "your-key-here",
    "api_key_param": "api_key"
  }
}
```

### Basic Authentication
```json
{
  "auth": {
    "type": "basic",
    "username": "your-username",
    "password": "your-password"
  }
}
```

### Custom Headers
```json
{
  "auth": {
    "type": "custom",
    "custom_headers": {
      "X-Custom-Auth": "custom-value",
      "X-Client-ID": "client-123"
    }
  }
}
```

## Parameter Locations

- **query**: Query string parameters (`?param=value`)
- **path**: Path parameters (`/users/{id}`)
- **header**: HTTP headers
- **body**: Request body (for POST, PUT, PATCH)

## Parameter Types

- **string**: Text values
- **integer**: Whole numbers
- **number**: Decimal numbers
- **boolean**: true/false
- **array**: Lists of values
- **object**: JSON objects

## Advanced Features

### Custom Timeouts
```json
{
  "timeout": 60.0  // Timeout in seconds
}
```

### Enum Values
```json
{
  "name": "status",
  "type": "string",
  "enum": ["active", "inactive", "pending"]
}
```

### Default Values
```json
{
  "name": "page",
  "type": "integer",
  "default": 1
}
```

## Error Handling

The server provides detailed error messages for:
- Missing required parameters
- HTTP errors (with status codes)
- Connection failures
- Authentication errors
- Invalid configurations

## Tips

1. **Test First**: Always use `test_api_connection` after registering an API
2. **Start Simple**: Begin with GET endpoints before moving to complex POST requests
3. **Check Auth**: Ensure your authentication credentials are correct
4. **Use Descriptions**: Provide clear descriptions for better AI understanding
5. **Handle Errors**: The server will report HTTP errors with details

## Troubleshooting

### Common Issues

1. **401 Unauthorized**: Check your authentication credentials
2. **404 Not Found**: Verify the base URL and endpoint paths
3. **Timeout Errors**: Increase the timeout value for slow APIs
4. **SSL Errors**: Some APIs may require specific SSL configurations

### Debug Mode

Run with verbose logging:
```bash
python saas_to_mcp.py --verbose
```

## Contributing

Feel free to extend this server with additional features:
- OAuth2 token refresh
- GraphQL support
- WebSocket endpoints
- Response caching
- Rate limiting
- Request retries

## License

MIT License - feel free to use and modify as needed.
