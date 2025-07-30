# MCP Server Creator 🏗️

A powerful Model Context Protocol (MCP) server that creates other MCP servers! This meta-server provides tools for dynamically generating FastMCP server configurations and Python code.

## Features

- **Dynamic Server Creation**: Create new MCP server configurations on the fly
- **Tool Builder**: Add custom tools with parameters, return types, and implementations
- **Resource Manager**: Add static and dynamic resources with template support
- **Code Generation**: Generate complete, runnable Python code for your servers
- **File Export**: Save generated servers directly to Python files
- **Example Templates**: Built-in example server to demonstrate capabilities

## Installation

1. Install the package from PyPI:
   ```bash
   pip install mcp-server-creator
   ```

2. Ensure you have FastMCP installed (it should be installed as a dependency, but you can also install it explicitly):
   ```bash
   pip install fastmcp
   ```

## Running the Server

Once installed, you can run the server using FastMCP, pointing to the installed module:

```bash
fastmcp run mcp_server_creator_package.mcp_server_creator
```
(Note: We might add a direct command-line entry point later for easier execution.)

## Quick Start

### 1. Create a Simple Server

```python
import asyncio
from fastmcp import Client

async def create_simple_server():
    client = Client("mcp_server_creator_package.mcp_server_creator")
    
    async with client:
        # Create server
        await client.call_tool("create_server", {
            "name": "My First Server",
            "description": "A simple MCP server"
        })
        
        # Add a tool
        await client.call_tool("add_tool", {
            "server_id": "my_first_server",
            "tool_name": "greet",
            "description": "Greet someone",
            "parameters": [{"name": "name", "type": "str"}],
            "return_type": "str",
            "implementation": 'return f"Hello, {name}!"'
        })
        
        # Generate and save
        await client.call_tool("save_server", {
            "server_id": "my_first_server",
            "filename": "my_first_server.py"
        })

asyncio.run(create_simple_server())
```

### 2. Run Your Generated Server

```bash
fastmcp run my_first_server.py
```

## Available Tools

### Server Management

#### `create_server`
Create a new MCP server configuration.

**Parameters:**
- `name` (str): Server name
- `description` (str): Server description
- `version` (str): Version number (default: "1.0.0")

#### `list_servers`
List all server configurations in memory.

#### `get_server_details`
Get detailed information about a specific server.

**Parameters:**
- `server_id` (str): ID of the server

### Tool Management

#### `add_tool`
Add a tool to an existing server.

**Parameters:**
- `server_id` (str): Target server ID
- `tool_name` (str): Name of the tool function
- `description` (str): Tool description
- `parameters` (List[Dict]): Parameter definitions
  - Each parameter: `{"name": "param_name", "type": "str", "default": "optional_default"}`
- `return_type` (str): Return type (default: "str")
- `is_async` (bool): Whether the tool is async (default: False)
- `implementation` (str): Python code for the tool body

### Resource Management

#### `add_resource`
Add a resource to an existing server.

**Parameters:**
- `server_id` (str): Target server ID
- `uri` (str): Resource URI (e.g., "data://config" or "items://{id}/details")
- `name` (str): Resource name
- `description` (str): Resource description
- `mime_type` (str): MIME type (default: "application/json")
- `is_template` (bool): Whether this is a template with parameters
- `implementation` (str): Python code that returns the resource data

### Code Generation

#### `generate_server_code`
Generate complete Python code for a server.

**Parameters:**
- `server_id` (str): Server to generate code for
- `include_comments` (bool): Include helpful comments (default: True)

#### `save_server`
Save generated server code to a file.

**Parameters:**
- `server_id` (str): Server to save
- `filename` (str): Output file path

### Utilities

#### `create_example_server`
Create a complete example Weather Service server to demonstrate capabilities.

## Available Resources

- `data://server-creator/info` - Information about the MCP Server Creator
- `data://servers/{server_id}/code` - Generated Python code for a specific server

## Advanced Example: Building a Complex Server

```python
async def create_advanced_server():
    client = Client("mcp_server_creator_package.mcp_server_creator")
    
    async with client:
        # Create server
        await client.call_tool("create_server", {
            "name": "Data Analytics Server",
            "description": "Server for data analysis operations"
        })
        
        # Add async tool with complex logic
        await client.call_tool("add_tool", {
            "server_id": "data_analytics_server",
            "tool_name": "analyze_dataset",
            "description": "Analyze a dataset and return statistics",
            "parameters": [
                {"name": "data", "type": "List[float]"},
                {"name": "include_outliers", "type": "bool", "default": "True"}
            ],
            "return_type": "dict",
            "is_async": True,
            "implementation": '''
    import statistics
    import asyncio
    
    # Simulate async processing
    await asyncio.sleep(0.1)
    
    # Calculate statistics
    stats = {
        "count": len(data),
        "mean": statistics.mean(data) if data else 0,
        "median": statistics.median(data) if data else 0,
        "stdev": statistics.stdev(data) if len(data) > 1 else 0
    }
    
    if not include_outliers and len(data) > 2:
        # Simple outlier removal (values beyond 2 std devs)
        mean = stats["mean"]
        stdev = stats["stdev"]
        filtered = [x for x in data if abs(x - mean) <= 2 * stdev]
        stats["filtered_count"] = len(filtered)
    
    return stats'''
        })
        
        # Add resource template
        await client.call_tool("add_resource", {
            "server_id": "data_analytics_server",
            "uri": "analysis://{dataset_id}/results",
            "name": "Analysis Results",
            "description": "Get analysis results for a dataset",
            "is_template": True,
            "implementation": '''
    # Simulated results lookup
    results = {
        "sales_2024": {
            "total_records": 1523,
            "trend": "increasing",
            "anomalies": 3
        },
        "customer_feedback": {
            "total_records": 892,
            "sentiment": "positive",
            "score": 4.2
        }
    }
    
    return results.get(dataset_id, {"error": "Dataset not found"})'''
        })
```

## Tips and Best Practices

1. **Server IDs**: Server IDs are automatically generated from the server name (lowercase, spaces replaced with underscores)

2. **Tool Parameters**: Use Python type hints syntax for parameter types:
   - Basic types: `str`, `int`, `float`, `bool`
   - Optional types: `str | None`
   - Collections: `List[str]`, `Dict[str, Any]`

3. **Async Tools**: Use `is_async=True` for tools that perform I/O operations (file reading, network requests, etc.)

4. **Resource Templates**: Use curly braces in URIs to create template parameters: `items://{item_id}/details`

5. **Implementation Code**: The implementation string should contain valid Python code that will be indented inside the function

## Workflow Example

1. **Design Phase**: Plan your server's tools and resources
2. **Create Server**: Use `create_server` to initialize
3. **Add Components**: Add tools and resources incrementally
4. **Test Generation**: Use `generate_server_code` to preview
5. **Save and Run**: Save to file and test with FastMCP

## Error Handling

The MCP Server Creator includes error handling for common issues:
- Duplicate server IDs
- Missing server configurations
- Invalid tool parameters
- File system errors during save operations

## Contributing

Feel free to extend the MCP Server Creator with additional features:
- Add support for prompts
- Include authentication configuration
- Add more sophisticated code templates
- Create a library of reusable components

## License

This project follows the same license as FastMCP.

---

Happy server creating! 🚀
