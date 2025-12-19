# MCP Registry API Reference

This document provides a complete reference for the MCP Registry REST API.

## Base URL

```
https://<registry-hostname>/api/v1
```

Replace `<registry-hostname>` with your OpenShift route hostname.

## Authentication

Current implementation does not require authentication. In production environments, implement OAuth2 or API key authentication.

## Common Headers

### Request Headers

```
Content-Type: application/json
Accept: application/json
```

### Response Headers

```
Content-Type: application/json
```

## Status Codes

The API uses standard HTTP status codes:

- `200 OK` - Request succeeded
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Endpoints

### Health Check

#### GET /health

Health check endpoint for monitoring.

**Response**

```json
{
  "status": "healthy"
}
```

**Example**

```bash
curl https://<registry-hostname>/health
```

---

#### GET /ready

Readiness probe endpoint.

**Response**

```json
{
  "status": "ready"
}
```

**Example**

```bash
curl https://<registry-hostname>/ready
```

---

### Tools Management

#### GET /api/v1/tools

List all tools in the registry.

**Response**

```json
{
  "tools": [
    {
      "name": "filesystem-tool",
      "version": "1.0.0",
      "description": "Tool for filesystem operations",
      "type": "mcp",
      "capabilities": [
        "read_file",
        "write_file",
        "list_directory"
      ],
      "configuration": {
        "basePath": "/tmp",
        "maxFileSize": "10MB"
      },
      "metadata": {
        "author": "MCP Community",
        "license": "Apache-2.0",
        "repository": "https://github.com/modelcontextprotocol/filesystem-tool"
      }
    }
  ]
}
```

**Example**

```bash
curl https://<registry-hostname>/api/v1/tools
```

---

#### GET /api/v1/tools/{tool_name}

Get details for a specific tool.

**Parameters**

- `tool_name` (path parameter) - Name of the tool

**Response**

Success (200):
```json
{
  "name": "filesystem-tool",
  "version": "1.0.0",
  "description": "Tool for filesystem operations",
  "type": "mcp",
  "capabilities": [
    "read_file",
    "write_file",
    "list_directory"
  ],
  "configuration": {
    "basePath": "/tmp",
    "maxFileSize": "10MB"
  },
  "metadata": {
    "author": "MCP Community",
    "license": "Apache-2.0",
    "repository": "https://github.com/modelcontextprotocol/filesystem-tool"
  }
}
```

Not Found (404):
```json
{
  "error": "Tool not found"
}
```

**Example**

```bash
curl https://<registry-hostname>/api/v1/tools/filesystem-tool
```

---

#### POST /api/v1/tools

Create a new tool in the registry.

**Request Body**

```json
{
  "name": "my-tool",
  "version": "1.0.0",
  "description": "My custom tool",
  "type": "mcp",
  "capabilities": [
    "capability1",
    "capability2"
  ],
  "configuration": {
    "setting1": "value1"
  },
  "metadata": {
    "author": "Developer Name",
    "license": "MIT"
  }
}
```

**Required Fields**

- `name` (string) - Unique tool name
- `version` (string) - Semantic version
- `description` (string) - Tool description
- `type` (string) - Tool type (usually "mcp")

**Optional Fields**

- `capabilities` (array) - List of tool capabilities
- `configuration` (object) - Tool-specific configuration
- `metadata` (object) - Additional metadata

**Response**

Success (201):
```json
{
  "message": "Tool created",
  "tool": {
    "name": "my-tool",
    "version": "1.0.0",
    "description": "My custom tool",
    "type": "mcp",
    "capabilities": [
      "capability1",
      "capability2"
    ],
    "configuration": {
      "setting1": "value1"
    },
    "metadata": {
      "author": "Developer Name",
      "license": "MIT"
    }
  }
}
```

Bad Request (400):
```json
{
  "error": "Tool name required"
}
```

**Example**

```bash
curl -X POST https://<registry-hostname>/api/v1/tools \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-tool",
    "version": "1.0.0",
    "description": "My custom tool",
    "type": "mcp",
    "capabilities": ["capability1"]
  }'
```

---

## Tool Schema

### Tool Object

A tool object represents an MCP tool with its configuration and metadata.

```json
{
  "name": "string (required)",
  "version": "string (required, semver format)",
  "description": "string (required)",
  "type": "string (required, typically 'mcp')",
  "capabilities": [
    "string (capability names)"
  ],
  "configuration": {
    "key": "value (tool-specific settings)"
  },
  "metadata": {
    "author": "string (author name)",
    "license": "string (license type)",
    "repository": "string (repository URL)",
    "created": "string (ISO 8601 date)",
    "updated": "string (ISO 8601 date)"
  }
}
```

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Unique identifier for the tool |
| version | string | Yes | Semantic version (e.g., "1.0.0") |
| description | string | Yes | Human-readable description |
| type | string | Yes | Tool type, typically "mcp" |
| capabilities | array | No | List of capabilities the tool provides |
| configuration | object | No | Tool-specific configuration options |
| metadata | object | No | Additional metadata about the tool |

### Capability Format

Capabilities are strings that describe what the tool can do:

```json
"capabilities": [
  "read_file",
  "write_file",
  "list_directory",
  "create_directory"
]
```

### Configuration Format

Configuration is a flexible object for tool-specific settings:

```json
"configuration": {
  "basePath": "/tmp",
  "maxFileSize": "10MB",
  "allowedExtensions": [".txt", ".md"],
  "timeout": 30
}
```

### Metadata Format

Metadata provides information about the tool:

```json
"metadata": {
  "author": "John Doe",
  "license": "Apache-2.0",
  "repository": "https://github.com/user/repo",
  "created": "2024-01-01T00:00:00Z",
  "updated": "2024-01-15T10:30:00Z",
  "tags": ["filesystem", "utility"],
  "homepage": "https://example.com/tool"
}
```

## Error Responses

All error responses follow this format:

```json
{
  "error": "Error message description"
}
```

### Common Errors

#### 400 Bad Request

```json
{
  "error": "Tool name required"
}
```

Occurs when required fields are missing or invalid.

#### 404 Not Found

```json
{
  "error": "Tool not found"
}
```

Occurs when requesting a tool that doesn't exist.

#### 500 Internal Server Error

```json
{
  "error": "Internal server error"
}
```

Occurs when the server encounters an unexpected error.

## Rate Limiting

Current implementation does not enforce rate limiting. For production:

- Recommended: 100 requests per minute per client
- Consider implementing token bucket algorithm
- Return `429 Too Many Requests` when limit exceeded

## Versioning

The API uses URL-based versioning:

- Current version: `v1`
- Base path: `/api/v1`

Future versions will be introduced as `/api/v2`, etc., maintaining backward compatibility.

## Examples

### Complete Workflow Example

```bash
# 1. Check registry health
curl https://registry.example.com/health

# 2. List existing tools
curl https://registry.example.com/api/v1/tools

# 3. Create a new tool
curl -X POST https://registry.example.com/api/v1/tools \
  -H "Content-Type: application/json" \
  -d '{
    "name": "example-tool",
    "version": "1.0.0",
    "description": "Example MCP tool",
    "type": "mcp",
    "capabilities": ["example_capability"],
    "metadata": {
      "author": "Demo User",
      "license": "MIT"
    }
  }'

# 4. Retrieve the created tool
curl https://registry.example.com/api/v1/tools/example-tool

# 5. List all tools again to see the new one
curl https://registry.example.com/api/v1/tools
```

### Using with Python

```python
import requests
import json

base_url = "https://registry.example.com/api/v1"

# List tools
response = requests.get(f"{base_url}/tools")
tools = response.json()["tools"]
print(f"Found {len(tools)} tools")

# Create a tool
new_tool = {
    "name": "my-python-tool",
    "version": "1.0.0",
    "description": "Created from Python",
    "type": "mcp",
    "capabilities": ["python_capability"]
}

response = requests.post(
    f"{base_url}/tools",
    json=new_tool,
    headers={"Content-Type": "application/json"}
)

if response.status_code == 201:
    print("Tool created successfully")
    print(json.dumps(response.json(), indent=2))
```

### Using with curl and jq

```bash
# Pretty-print JSON responses
curl -s https://registry.example.com/api/v1/tools | jq '.'

# Get specific field
curl -s https://registry.example.com/api/v1/tools/filesystem-tool | jq '.version'

# Filter tools by capability
curl -s https://registry.example.com/api/v1/tools | jq '.tools[] | select(.capabilities[] | contains("read_file"))'
```

## Future Enhancements

Planned API enhancements:

1. **Tool Updates**: `PUT /api/v1/tools/{tool_name}`
2. **Tool Deletion**: `DELETE /api/v1/tools/{tool_name}`
3. **Search**: `GET /api/v1/tools?search=query`
4. **Filtering**: `GET /api/v1/tools?capability=read_file`
5. **Pagination**: `GET /api/v1/tools?page=1&limit=10`
6. **Tool Versions**: `GET /api/v1/tools/{tool_name}/versions`
7. **Authentication**: OAuth2/JWT support
8. **Webhooks**: Event notifications for tool changes

## Related Documentation

- [Architecture Overview](architecture.md)
- [Troubleshooting Guide](troubleshooting.md)
- [MCP Specification](https://modelcontextprotocol.io/)
