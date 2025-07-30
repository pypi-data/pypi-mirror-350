# MCP Server Creator 🏗️

[![PyPI version](https://badge.fury.io/py/mcp-server-creator.svg)](https://badge.fury.io/py/mcp-server-creator)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful Model Context Protocol (MCP) server that creates other MCP servers! This meta-server provides tools for dynamically generating FastMCP server configurations and Python code.

## 🚀 Quick Start

### Install with pip

```bash
pip install mcp-server-creator
```

### Run with uvx (recommended)

```bash
uvx mcp-server-creator
```

### Run as a module

```bash
python -m mcp_server_creator
```

## Features

- **Dynamic Server Creation**: Create new MCP server configurations on the fly
- **Tool Builder**: Add custom tools with parameters, return types, and implementations
- **Resource Manager**: Add static and dynamic resources with template support
- **Code Generation**: Generate complete, runnable Python code for your servers
- **File Export**: Save generated servers directly to Python files
- **Example Templates**: Built-in example server to demonstrate capabilities

## Usage

### As an MCP Server

The MCP Server Creator is itself an MCP server that can be used with Claude Desktop or any MCP client.

#### Claude Desktop Configuration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mcp-server-creator": {
      "command": "uvx",
      "args": ["mcp-server-creator"]
    }
  }
}
```

### Programmatic Usage

```python
from mcp_server_creator import create_server, add_tool, generate_server_code

# Create a new server configuration
result = create_server(
    name="My API Server",
    description="A custom API integration server",
    version="1.0.0"
)

# Add a tool
add_tool(
    server_id="my_api_server",
    tool_name="fetch_data",
    description="Fetch data from the API",
    parameters=[{"name": "endpoint", "type": "str"}],
    return_type="dict",
    implementation='return {"data": f"Fetched from {endpoint}"}'
)

# Generate the code
code = generate_server_code("my_api_server")
print(code)
```

## Available Tools

### Server Management

- `create_server`: Create a new MCP server configuration
- `list_servers`: List all server configurations in memory
- `get_server_details`: Get detailed information about a specific server

### Tool Management

- `add_tool`: Add a tool to an existing server
  - Supports both sync and async tools
  - Custom parameter definitions with types and defaults
  - Automatic import management

### Resource Management

- `add_resource`: Add a resource to an existing server
  - Static resources for fixed data
  - Dynamic resource templates with parameters
  - Custom MIME types

### Code Generation

- `generate_server_code`: Generate complete Python code for a server
- `save_server`: Save generated server code to a file
- `create_example_server`: Create a complete example Weather Service

## Example: Creating a Weather Service

```python
import asyncio
from mcp_server_creator import create_server, add_tool, add_resource, save_server

async def create_weather_service():
    # Create the server
    create_server(
        name="Weather Service",
        description="Get weather information",
        version="1.0.0"
    )
    
    # Add a weather tool
    add_tool(
        server_id="weather_service",
        tool_name="get_weather",
        description="Get current weather for a city",
        parameters=[
            {"name": "city", "type": "str"},
            {"name": "units", "type": "str", "default": '"celsius"'}
        ],
        return_type="dict",
        is_async=True,
        implementation='''
    # Your weather API logic here
    return {
        "city": city,
        "temperature": 20,
        "units": units,
        "condition": "sunny"
    }'''
    )
    
    # Add a resource
    add_resource(
        server_id="weather_service",
        uri="weather://{city}/current",
        name="Current Weather",
        description="Get current weather data",
        is_template=True,
        implementation='return {"city": city, "weather": "sunny"}'
    )
    
    # Save to file
    await save_server("weather_service", "weather_service.py")

# Run the creation
asyncio.run(create_weather_service())
```

## Development

### Setup

```bash
git clone https://github.com/GongRzhe/mcp-server-creator.git
cd mcp-server-creator
pip install -e .
```

### Testing

```bash
python test_mcp_creator.py
```

## Requirements

- Python 3.8+
- FastMCP >= 0.1.0

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

GongRzhe - [gongrzhe@gmail.com](mailto:gongrzhe@gmail.com)

## Links

- [GitHub Repository](https://github.com/GongRzhe/mcp-server-creator)
- [PyPI Package](https://pypi.org/project/mcp-server-creator/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Model Context Protocol](https://modelcontextprotocol.io)
