# MCP Server Creator - Quick Reference 🚀

## Common Commands

### 1. Basic Server Creation Flow
```python
# Create server
await client.call_tool("create_server", {
    "name": "My Server",
    "description": "Description here"
})

# Add a tool
await client.call_tool("add_tool", {
    "server_id": "my_server",
    "tool_name": "my_tool",
    "description": "What it does",
    "parameters": [{"name": "param1", "type": "str"}],
    "implementation": "return f'Result: {param1}'"
})

# Generate code
code = await client.call_tool("generate_server_code", {
    "server_id": "my_server"
})

# Save to file
await client.call_tool("save_server", {
    "server_id": "my_server",
    "filename": "my_server.py"
})
```

### 2. Parameter Types Reference
```python
# Basic types
{"name": "text", "type": "str"}
{"name": "number", "type": "int"}
{"name": "decimal", "type": "float"}
{"name": "flag", "type": "bool"}

# Optional types
{"name": "optional_text", "type": "str | None", "default": "None"}

# Collections
{"name": "items", "type": "List[str]"}
{"name": "mapping", "type": "Dict[str, Any]"}

# With defaults
{"name": "limit", "type": "int", "default": "10"}
{"name": "enabled", "type": "bool", "default": "True"}
```

### 3. Tool Implementation Examples

#### Simple Tool
```python
"implementation": """
    result = process_data(input_param)
    return f"Processed: {result}"
"""
```

#### Tool with Error Handling
```python
"implementation": """
    try:
        result = risky_operation(param)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
"""
```

#### Async Tool with External API
```python
"is_async": True,
"implementation": """
    import aiohttp
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.example.com/{endpoint}") as response:
            data = await response.json()
            return data
"""
```

### 4. Resource Examples

#### Static Resource
```python
await client.call_tool("add_resource", {
    "server_id": "my_server",
    "uri": "data://config",
    "name": "Configuration",
    "implementation": """
    return {
        "version": "1.0",
        "features": ["feature1", "feature2"],
        "settings": {"debug": False}
    }
"""
})
```

#### Resource Template
```python
await client.call_tool("add_resource", {
    "server_id": "my_server",
    "uri": "items://{item_id}/info",
    "name": "Item Information",
    "is_template": True,
    "implementation": """
    items_db = {
        "item1": {"name": "First", "price": 10},
        "item2": {"name": "Second", "price": 20}
    }
    
    if item_id in items_db:
        return items_db[item_id]
    else:
        return {"error": f"Item {item_id} not found"}
"""
})
```

## Common Patterns

### 1. Database-like Server
```python
# Create
await client.call_tool("add_tool", {
    "server_id": "db_server",
    "tool_name": "create_record",
    "parameters": [{"name": "data", "type": "dict"}],
    "implementation": "# Save to database"
})

# Read
await client.call_tool("add_tool", {
    "server_id": "db_server",
    "tool_name": "get_record",
    "parameters": [{"name": "id", "type": "str"}],
    "implementation": "# Fetch from database"
})

# Update
await client.call_tool("add_tool", {
    "server_id": "db_server",
    "tool_name": "update_record",
    "parameters": [
        {"name": "id", "type": "str"},
        {"name": "updates", "type": "dict"}
    ],
    "implementation": "# Update in database"
})

# Delete
await client.call_tool("add_tool", {
    "server_id": "db_server",
    "tool_name": "delete_record",
    "parameters": [{"name": "id", "type": "str"}],
    "implementation": "# Delete from database"
})
```

### 2. API Wrapper Server
```python
# Base configuration
await client.call_tool("add_resource", {
    "server_id": "api_server",
    "uri": "data://api/config",
    "name": "API Configuration",
    "implementation": """
    return {
        "base_url": "https://api.example.com",
        "version": "v1",
        "timeout": 30
    }
"""
})

# API call tool
await client.call_tool("add_tool", {
    "server_id": "api_server",
    "tool_name": "api_request",
    "parameters": [
        {"name": "endpoint", "type": "str"},
        {"name": "method", "type": "str", "default": '"GET"'},
        {"name": "data", "type": "dict | None", "default": "None"}
    ],
    "is_async": True,
    "implementation": """
    import aiohttp
    
    config = {"base_url": "https://api.example.com"}
    url = f"{config['base_url']}/{endpoint}"
    
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url, json=data) as response:
            return await response.json()
"""
})
```

### 3. File Processing Server
```python
# File reader
await client.call_tool("add_tool", {
    "server_id": "file_server",
    "tool_name": "read_file",
    "parameters": [
        {"name": "filepath", "type": "str"},
        {"name": "encoding", "type": "str", "default": '"utf-8"'}
    ],
    "is_async": True,
    "implementation": """
    import aiofiles
    
    try:
        async with aiofiles.open(filepath, mode='r', encoding=encoding) as f:
            content = await f.read()
        return {"success": True, "content": content}
    except Exception as e:
        return {"success": False, "error": str(e)}
"""
})
```

## Tips

1. **Server IDs**: Automatically generated from name (lowercase, spaces → underscores)
2. **Async Tools**: Use for I/O operations (file, network, database)
3. **Resource URIs**: Use `://` for static, `://{param}/` for templates
4. **Imports**: Added automatically for common cases (asyncio for async tools)
5. **Testing**: Use the test script to verify your server before deployment

## Debugging

```python
# List all servers
servers = await client.call_tool("list_servers", {})

# Get detailed info
details = await client.call_tool("get_server_details", {
    "server_id": "my_server"
})

# Preview generated code
code = await client.call_tool("generate_server_code", {
    "server_id": "my_server"
})
print(code[0].text)
```
