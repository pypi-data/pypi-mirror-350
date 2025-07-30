# SaaS-to-MCP Server Testing Guide

This guide demonstrates how to use the **saas-to-mcp MCP server** to register and test various API endpoints with different authentication methods. We'll use a comprehensive FastAPI demo application as our example.

## 🎯 Overview

The saas-to-mcp MCP server provides tools to:
- **Register APIs** with different authentication methods
- **Call registered APIs** dynamically
- **Manage API configurations** and schemas
- **Test various authentication patterns**

## 🚀 Setup

### 1. Start the Demo FastAPI Application

First, create and run a FastAPI demo application with multiple authentication methods:

```bash
# Install dependencies
pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt] python-multipart strawberry-graphql[fastapi] aiofiles

# Run the application
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The demo application will be available at:
- **API Documentation:** http://localhost:8000/docs
- **GraphQL Playground:** http://localhost:8000/graphql
- **WebSocket Chat:** http://localhost:8000/chat

### 2. Test Credentials

The demo includes these test credentials:
- **JWT Auth:** username: `testuser`, password: `secret`
- **HTTP Basic:** username: `testuser`, password: `secret`
- **API Key:** `super-secret-api-key`
- **Custom Header:** `X-Token: super-secret-token`

## 📝 Registering APIs

### Basic API Registration (No Auth)

```python
register_api({
    "name": "FastAPI Demo - System",
    "base_url": "http://localhost:8000",
    "auth": {"type": "none"},
    "endpoints": [
        {
            "name": "health_check",
            "path": "/health",
            "method": "GET",
            "description": "Health check endpoint",
            "parameters": []
        }
    ],
    "description": "System and public endpoints"
})
```

### JWT Bearer Token Authentication

```python
register_api({
    "name": "FastAPI Demo - JWT Protected",
    "base_url": "http://localhost:8000",
    "auth": {"type": "bearer", "header": "Authorization"},
    "headers": {"Authorization": "Bearer {token}"},
    "endpoints": [
        {
            "name": "get_current_user",
            "path": "/users/me",
            "method": "GET",
            "description": "Get current authenticated user information",
            "parameters": []
        },
        {
            "name": "list_items",
            "path": "/items",
            "method": "GET",
            "parameters": [
                {
                    "name": "skip",
                    "type": "query",
                    "required": false,
                    "description": "Number of items to skip (default: 0)"
                }
            ],
            "description": "Get items for current user"
        }
    ],
    "description": "Endpoints requiring JWT authentication"
})
```

### HTTP Basic Authentication

```python
register_api({
    "name": "FastAPI Demo - Basic Auth",
    "base_url": "http://localhost:8000",
    "auth": {
        "type": "basic",
        "username": "testuser",
        "password": "secret"
    },
    "endpoints": [
        {
            "name": "get_user_basic",
            "path": "/users/me/basic",
            "method": "GET",
            "description": "Get current user info using HTTP Basic Auth",
            "parameters": []
        }
    ],
    "description": "Endpoints using HTTP Basic Authentication"
})
```

### API Key Authentication

```python
register_api({
    "name": "FastAPI Demo - API Key",
    "base_url": "http://localhost:8000",
    "auth": {
        "type": "api_key",
        "key": "super-secret-api-key",
        "header": "X-API-Key"
    },
    "headers": {"X-API-Key": "super-secret-api-key"},
    "endpoints": [
        {
            "name": "protected_api_key",
            "path": "/protected/api-key",
            "method": "GET",
            "description": "Protected endpoint using API Key",
            "parameters": []
        },
        {
            "name": "get_metrics",
            "path": "/metrics",
            "method": "GET",
            "description": "Get system metrics (requires API key)",
            "parameters": []
        }
    ],
    "description": "Endpoints using API Key authentication"
})
```

### Custom Header Authentication

```python
register_api({
    "name": "FastAPI Demo - Custom Header",
    "base_url": "http://localhost:8000",
    "auth": {"type": "custom"},
    "headers": {"X-Token": "super-secret-token"},
    "endpoints": [
        {
            "name": "protected_custom_header",
            "path": "/protected/custom-header",
            "method": "GET",
            "description": "Protected endpoint using custom X-Token header",
            "parameters": []
        }
    ],
    "description": "Endpoints using custom header authentication"
})
```

### GraphQL API Registration

```python
register_api({
    "name": "FastAPI Demo - GraphQL",
    "base_url": "http://localhost:8000",
    "auth": {"type": "none"},
    "headers": {"Content-Type": "application/json"},
    "endpoints": [
        {
            "name": "graphql_query",
            "path": "/graphql",
            "method": "POST",
            "parameters": [
                {
                    "name": "query",
                    "type": "json",
                    "required": true,
                    "description": "GraphQL query string"
                }
            ],
            "description": "Execute GraphQL queries and mutations"
        }
    ],
    "description": "GraphQL API endpoints"
})
```

### File Upload/Download APIs

```python
register_api({
    "name": "FastAPI Demo - File Operations",
    "base_url": "http://localhost:8000",
    "auth": {"type": "bearer", "header": "Authorization"},
    "headers": {"Authorization": "Bearer {token}"},
    "endpoints": [
        {
            "name": "upload_file",
            "path": "/upload",
            "method": "POST",
            "parameters": [
                {
                    "name": "file",
                    "type": "file",
                    "required": true,
                    "description": "File to upload"
                }
            ],
            "description": "Upload file (requires JWT authentication)"
        },
        {
            "name": "download_file",
            "path": "/download/{filename}",
            "method": "GET",
            "parameters": [
                {
                    "name": "filename",
                    "type": "path",
                    "required": true,
                    "description": "Name of file to download"
                }
            ],
            "description": "Download file (requires JWT authentication)"
        }
    ],
    "description": "File upload and download with JWT authentication"
})
```

## 🧪 Testing Registered APIs

### 1. List All Registered APIs

```python
list_apis()
```

This returns all registered API configurations with their endpoints and authentication methods.

### 2. Test Public Endpoints

```python
# Health check (no authentication required)
call_api("FastAPI Demo - System", "health_check", {})

# Expected response:
{
    "success": true,
    "data": {
        "status": "healthy",
        "timestamp": "2025-05-26T16:04:32.513188"
    }
}
```

### 3. Test API Key Authentication

```python
# Protected endpoint with API key
call_api("FastAPI Demo - API Key", "protected_api_key", {})

# Expected response:
{
    "success": true,
    "data": {
        "message": "Access granted",
        "user": "admin"
    }
}

# System metrics with API key
call_api("FastAPI Demo - API Key", "get_metrics", {})

# Expected response:
{
    "success": true,
    "data": {
        "total_users": 2,
        "total_items": 4,
        "active_connections": 0,
        "uptime": "unknown"
    }
}
```

### 4. Test Custom Header Authentication

```python
# Protected endpoint with custom header
call_api("FastAPI Demo - Custom Header", "protected_custom_header", {})

# Expected response:
{
    "success": true,
    "data": {
        "message": "Access granted with custom header",
        "token": "super-secret-token"
    }
}
```

### 5. Test Rate Limiting

```python
# Rate-limited endpoint (10 requests per minute)
call_api("FastAPI Demo - System", "rate_limited", {})

# Expected response:
{
    "success": true,
    "data": {
        "message": "Request successful",
        "remaining": 9
    }
}
```

### 6. Test JWT Authentication (requires token)

First, get a JWT token:
```python
# Note: This requires form data format which may need special handling
call_api("FastAPI Demo - Authentication", "get_jwt_token", {
    "username": "testuser",
    "password": "secret"
})
```

Then use the token for protected endpoints:
```python
# Get current user info (requires JWT token)
call_api("FastAPI Demo - JWT Protected", "get_current_user", {})

# List user's items
call_api("FastAPI Demo - JWT Protected", "list_items", {
    "skip": 0,
    "limit": 10
})
```

## 🔍 API Schema Inspection

Get detailed information about an API's schema:

```python
get_api_schema("FastAPI Demo - API Key")
get_api_schema("FastAPI Demo - JWT Protected", "get_current_user")
```

## 🛠️ API Management

### Test API Connection

```python
test_api_connection("FastAPI Demo - System")
```

### Unregister APIs

```python
unregister_api("FastAPI Demo - System")
```

## 🎯 Authentication Patterns Demonstrated

### 1. **No Authentication**
- Public endpoints
- Health checks
- Documentation

### 2. **Bearer Token (JWT)**
- OAuth2 password flow
- Authorization header
- User-specific data access

### 3. **HTTP Basic Authentication**
- Username/password encoded in header
- Simple authentication method

### 4. **API Key Authentication**
- Header-based: `X-API-Key`
- Query parameter: `?api_key=value`
- Cookie-based authentication

### 5. **Custom Headers**
- Application-specific headers
- Custom token validation

## 📊 API Types Covered

### **REST APIs**
- Standard HTTP methods (GET, POST, PUT, DELETE)
- Path parameters and query strings
- JSON request/response bodies

### **GraphQL APIs**
- Query and mutation operations
- Structured data requests
- Interactive playground

### **File Operations**
- Multipart file uploads
- File downloads with authentication
- Binary data handling

### **WebSocket APIs**
- Real-time bidirectional communication
- Authentication via query parameters
- Connection management

### **System APIs**
- Health monitoring
- Metrics collection
- Rate limiting

## 🚀 Advanced Features

### **Middleware Integration**
- CORS configuration
- Request timing headers
- Security headers
- Rate limiting

### **Error Handling**
- Structured error responses
- Authentication failures
- Validation errors

### **Documentation**
- Auto-generated OpenAPI specs
- Interactive Swagger UI
- Alternative ReDoc interface

## 💡 Best Practices

1. **Authentication Security**
   - Use HTTPS in production
   - Rotate API keys regularly
   - Implement proper token expiration

2. **API Design**
   - Follow RESTful conventions
   - Use appropriate HTTP status codes
   - Provide clear error messages

3. **Testing**
   - Test all authentication methods
   - Verify error scenarios
   - Check rate limiting behavior

4. **Configuration**
   - Use environment variables for secrets
   - Separate configs per environment
   - Document authentication requirements

## 🔧 Troubleshooting

### Common Issues

1. **Authentication Failures**
   - Verify credentials are correct
   - Check header format
   - Ensure API is running

2. **Connection Errors**
   - Confirm base URL is accessible
   - Check network connectivity
   - Verify port is open

3. **Parameter Issues**
   - Match required parameter types
   - Use correct parameter names
   - Handle optional parameters properly

### Debug Tips

- Use `test_api_connection()` first
- Check `get_api_schema()` for parameter details
- Review error messages for specific issues
- Test with simple endpoints before complex ones

## 📝 Summary

The saas-to-mcp MCP server provides a powerful way to:

- **Register APIs** with various authentication methods
- **Test endpoints** dynamically without manual setup
- **Manage API configurations** centrally
- **Handle different authentication patterns** seamlessly
- **Support multiple API types** (REST, GraphQL, WebSocket, Files)

This makes it an excellent tool for API integration testing, development workflows, and automating API interactions across different services and authentication systems.
