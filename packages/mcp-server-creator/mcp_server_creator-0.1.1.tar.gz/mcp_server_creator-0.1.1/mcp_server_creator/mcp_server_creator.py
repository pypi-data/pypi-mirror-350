#!/usr/bin/env python3
"""
MCP Server Creator - An MCP server that creates other MCP servers
This is a meta-MCP server that provides tools for generating FastMCP server code.
"""

import json
import textwrap
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime

from fastmcp import FastMCP, Context

# Initialize the MCP Server Creator
mcp = FastMCP(
    "MCP Server Creator 🏗️",
    instructions="""
    This server helps you create other MCP servers using FastMCP.
    Use the tools to:
    1. Create new server configurations
    2. Add tools with custom logic
    3. Add resources (static and dynamic)
    4. Generate Python code
    5. Save servers to files
    """
)

# In-memory storage for server configurations
@dataclass
class ToolConfig:
    name: str
    description: str
    parameters: List[Dict[str, Any]]
    return_type: str
    is_async: bool
    implementation: str

@dataclass
class ResourceConfig:
    uri: str
    name: str
    description: str
    mime_type: str
    is_template: bool
    parameters: List[str]
    implementation: str

@dataclass
class ServerConfig:
    name: str
    description: str
    version: str = "1.0.0"
    tools: Dict[str, ToolConfig] = field(default_factory=dict)
    resources: Dict[str, ResourceConfig] = field(default_factory=dict)
    imports: List[str] = field(default_factory=lambda: ["from fastmcp import FastMCP, Context"])
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

# Global storage for server configurations
servers: Dict[str, ServerConfig] = {}

@mcp.tool()
def create_server(
    name: str,
    description: str = "",
    version: str = "1.0.0"
) -> Dict[str, Any]:
    """
    Create a new MCP server configuration.
    
    Args:
        name: The name of the server (e.g., "Weather Service")
        description: A description of what the server does
        version: Version number of the server
    
    Returns:
        Server configuration details
    """
    server_id = name.lower().replace(" ", "_")
    
    if server_id in servers:
        return {
            "success": False,
            "error": f"Server '{server_id}' already exists"
        }
    
    servers[server_id] = ServerConfig(
        name=name,
        description=description or f"MCP server for {name}",
        version=version
    )
    
    return {
        "success": True,
        "server_id": server_id,
        "message": f"Created server configuration for '{name}'",
        "config": {
            "name": name,
            "description": servers[server_id].description,
            "version": version
        }
    }

@mcp.tool()
def add_tool(
    server_id: str,
    tool_name: str,
    description: str,
    parameters: List[Dict[str, str]],
    return_type: str = "str",
    is_async: bool = False,
    implementation: Optional[str] = None
) -> Dict[str, Any]:
    """
    Add a tool to an existing server configuration.
    
    Args:
        server_id: ID of the server to add the tool to
        tool_name: Name of the tool function
        description: Description of what the tool does
        parameters: List of parameter definitions, each with 'name', 'type', and optional 'default'
        return_type: Return type of the tool (e.g., "str", "dict", "int")
        is_async: Whether the tool should be async
        implementation: Custom implementation code (if not provided, generates a placeholder)
    
    Returns:
        Tool configuration details
    """
    if server_id not in servers:
        return {
            "success": False,
            "error": f"Server '{server_id}' not found"
        }
    
    server = servers[server_id]
    
    if tool_name in server.tools:
        return {
            "success": False,
            "error": f"Tool '{tool_name}' already exists in server '{server_id}'"
        }
    
    # Generate default implementation if not provided
    if not implementation:
        param_names = [p["name"] for p in parameters]
        implementation = f"""
    # TODO: Implement {tool_name} logic
    result = {{
        "tool": "{tool_name}",
        "parameters": {{{", ".join([f'"{p}": {p}' for p in param_names])}}}
    }}
    return result"""
    
    server.tools[tool_name] = ToolConfig(
        name=tool_name,
        description=description,
        parameters=parameters,
        return_type=return_type,
        is_async=is_async,
        implementation=implementation.strip()
    )
    
    # Add necessary imports for async tools
    if is_async and "import asyncio" not in server.imports:
        server.imports.append("import asyncio")
    
    return {
        "success": True,
        "message": f"Added tool '{tool_name}' to server '{server_id}'",
        "tool": {
            "name": tool_name,
            "description": description,
            "is_async": is_async,
            "parameters": parameters
        }
    }

@mcp.tool()
def add_resource(
    server_id: str,
    uri: str,
    name: str,
    description: str = "",
    mime_type: str = "application/json",
    is_template: bool = False,
    implementation: Optional[str] = None
) -> Dict[str, Any]:
    """
    Add a resource to an existing server configuration.
    
    Args:
        server_id: ID of the server to add the resource to
        uri: URI for the resource (e.g., "data://config" or "weather://{city}/current" for templates)
        name: Name of the resource
        description: Description of what the resource provides
        mime_type: MIME type of the resource
        is_template: Whether this is a resource template with parameters
        implementation: Custom implementation code
    
    Returns:
        Resource configuration details
    """
    if server_id not in servers:
        return {
            "success": False,
            "error": f"Server '{server_id}' not found"
        }
    
    server = servers[server_id]
    
    # Extract parameters from URI if it's a template
    parameters = []
    if is_template:
        import re
        parameters = re.findall(r'\{(\w+)\}', uri)
    
    # Generate function name from URI
    func_name = uri.replace("://", "_").replace("/", "_").replace("{", "").replace("}", "")
    func_name = "get_" + func_name.strip("_")
    
    # Generate default implementation
    if not implementation:
        if parameters:
            param_dict = ", ".join([f'"{p}": {p}' for p in parameters])
            implementation = f"""
    # TODO: Implement resource logic
    return {{
        "uri": "{uri}",
        {param_dict},
        "data": "Resource data here"
    }}"""
        else:
            implementation = f"""
    # TODO: Implement resource logic
    return {{
        "uri": "{uri}",
        "data": "Static resource data here"
    }}"""
    
    server.resources[uri] = ResourceConfig(
        uri=uri,
        name=name,
        description=description or f"Resource at {uri}",
        mime_type=mime_type,
        is_template=is_template,
        parameters=parameters,
        implementation=implementation.strip()
    )
    
    return {
        "success": True,
        "message": f"Added resource '{uri}' to server '{server_id}'",
        "resource": {
            "uri": uri,
            "name": name,
            "is_template": is_template,
            "parameters": parameters if is_template else []
        }
    }

@mcp.tool()
def generate_server_code(server_id: str, include_comments: bool = True) -> str:
    """
    Generate the complete Python code for an MCP server.
    
    Args:
        server_id: ID of the server to generate code for
        include_comments: Whether to include helpful comments in the generated code
    
    Returns:
        Complete Python code for the MCP server
    """
    if server_id not in servers:
        return f"Error: Server '{server_id}' not found"
    
    server = servers[server_id]
    
    # Start building the code
    code_parts = []
    
    # Header
    code_parts.append('#!/usr/bin/env python3')
    code_parts.append('"""')
    code_parts.append(f'{server.name} - {server.description}')
    code_parts.append(f'Version: {server.version}')
    code_parts.append(f'Generated by MCP Server Creator on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    code_parts.append('"""')
    code_parts.append('')
    
    # Imports
    for imp in server.imports:
        code_parts.append(imp)
    code_parts.append('')
    
    # Initialize MCP server
    code_parts.append(f'# Initialize the MCP server')
    code_parts.append(f'mcp = FastMCP(')
    code_parts.append(f'    "{server.name}",')
    code_parts.append(f'    instructions="""{server.description}"""')
    code_parts.append(f')')
    code_parts.append('')
    
    # Add tools
    if server.tools:
        if include_comments:
            code_parts.append('# Tools')
        for tool in server.tools.values():
            code_parts.append('')
            code_parts.append('@mcp.tool()')
            
            # Build function signature
            func_def = "async def" if tool.is_async else "def"
            params = []
            for param in tool.parameters:
                param_str = f"{param['name']}: {param['type']}"
                if 'default' in param:
                    param_str += f" = {param['default']}"
                params.append(param_str)
            
            params_str = ", ".join(params)
            code_parts.append(f'{func_def} {tool.name}({params_str}) -> {tool.return_type}:')
            code_parts.append(f'    """{tool.description}"""')
            
            # Add implementation
            for line in tool.implementation.split('\n'):
                code_parts.append(line if line.strip() else '')
    
    # Add resources
    if server.resources:
        if include_comments:
            code_parts.append('')
            code_parts.append('# Resources')
        for resource in server.resources.values():
            code_parts.append('')
            
            # Build decorator
            decorator_args = [f'"{resource.uri}"']
            if resource.mime_type != "application/json":
                decorator_args.append(f'mime_type="{resource.mime_type}"')
            
            code_parts.append(f'@mcp.resource({", ".join(decorator_args)})')
            
            # Build function
            func_name = resource.uri.replace("://", "_").replace("/", "_").replace("{", "").replace("}", "")
            func_name = "get_" + func_name.strip("_")
            
            params = []
            if resource.parameters:
                params = [f"{p}: str" for p in resource.parameters]
            
            params_str = ", ".join(params)
            code_parts.append(f'def {func_name}({params_str}) -> dict:')
            code_parts.append(f'    """{resource.description}"""')
            
            # Add implementation
            for line in resource.implementation.split('\n'):
                code_parts.append(line if line.strip() else '')
    
    # Add main block
    code_parts.append('')
    code_parts.append('')
    code_parts.append('if __name__ == "__main__":')
    code_parts.append('    mcp.run()')
    
    return '\n'.join(code_parts)

@mcp.tool()
async def save_server(
    server_id: str,
    filename: str,
    ctx: Context
) -> Dict[str, Any]:
    """
    Save the generated server code to a file.
    
    Args:
        server_id: ID of the server to save
        filename: Path where to save the Python file
        ctx: MCP context for logging
    
    Returns:
        Save operation result
    """
    if server_id not in servers:
        return {
            "success": False,
            "error": f"Server '{server_id}' not found"
        }
    
    try:
        # Generate the code
        code = generate_server_code(server_id)
        
        # Create path object
        file_path = Path(filename)
        
        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the file
        file_path.write_text(code)
        
        # Make it executable on Unix-like systems
        try:
            import os
            import stat
            os.chmod(file_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
        except:
            pass
        
        await ctx.info(f"Successfully saved server to {file_path}")
        
        return {
            "success": True,
            "message": f"Server saved to {file_path}",
            "path": str(file_path.absolute()),
            "size": len(code)
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to save server: {str(e)}"
        }

@mcp.tool()
def list_servers() -> List[Dict[str, Any]]:
    """
    List all server configurations currently in memory.
    
    Returns:
        List of server configurations
    """
    return [
        {
            "server_id": server_id,
            "name": config.name,
            "description": config.description,
            "version": config.version,
            "tools_count": len(config.tools),
            "resources_count": len(config.resources),
            "created_at": config.created_at
        }
        for server_id, config in servers.items()
    ]

@mcp.tool()
def get_server_details(server_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific server configuration.
    
    Args:
        server_id: ID of the server to get details for
    
    Returns:
        Detailed server configuration
    """
    if server_id not in servers:
        return {"error": f"Server '{server_id}' not found"}
    
    server = servers[server_id]
    
    return {
        "server_id": server_id,
        "name": server.name,
        "description": server.description,
        "version": server.version,
        "created_at": server.created_at,
        "tools": [
            {
                "name": tool.name,
                "description": tool.description,
                "is_async": tool.is_async,
                "parameters": tool.parameters,
                "return_type": tool.return_type
            }
            for tool in server.tools.values()
        ],
        "resources": [
            {
                "uri": resource.uri,
                "name": resource.name,
                "description": resource.description,
                "is_template": resource.is_template,
                "parameters": resource.parameters,
                "mime_type": resource.mime_type
            }
            for resource in server.resources.values()
        ]
    }

@mcp.tool()
def create_example_server() -> Dict[str, Any]:
    """
    Create an example server configuration to demonstrate the MCP Server Creator capabilities.
    
    Returns:
        Details about the created example server
    """
    # Create a weather service example
    create_server(
        name="Weather Service",
        description="A simple weather information service",
        version="1.0.0"
    )
    
    # Add tools
    add_tool(
        server_id="weather_service",
        tool_name="get_current_weather",
        description="Get the current weather for a city",
        parameters=[
            {"name": "city", "type": "str"},
            {"name": "units", "type": "str", "default": '"celsius"'}
        ],
        return_type="dict",
        is_async=True,
        implementation="""
    # Simulated weather data
    weather_data = {
        "london": {"temp": 15, "condition": "cloudy"},
        "new york": {"temp": 22, "condition": "sunny"},
        "tokyo": {"temp": 18, "condition": "rainy"}
    }
    
    city_lower = city.lower()
    if city_lower in weather_data:
        data = weather_data[city_lower]
        temp = data["temp"]
        if units == "fahrenheit":
            temp = (temp * 9/5) + 32
        
        return {
            "city": city,
            "temperature": temp,
            "units": units,
            "condition": data["condition"]
        }
    else:
        return {
            "error": f"Weather data not available for {city}"
        }"""
    )
    
    add_tool(
        server_id="weather_service",
        tool_name="get_forecast",
        description="Get weather forecast for the next N days",
        parameters=[
            {"name": "city", "type": "str"},
            {"name": "days", "type": "int", "default": "3"}
        ],
        return_type="dict",
        implementation="""
    # Simple forecast simulation
    import random
    
    conditions = ["sunny", "cloudy", "rainy", "partly cloudy"]
    forecast = []
    
    for day in range(days):
        forecast.append({
            "day": day + 1,
            "high": random.randint(15, 30),
            "low": random.randint(5, 20),
            "condition": random.choice(conditions)
        })
    
    return {
        "city": city,
        "days": days,
        "forecast": forecast
    }"""
    )
    
    # Add resources
    add_resource(
        server_id="weather_service",
        uri="data://cities/supported",
        name="Supported Cities",
        description="List of cities with weather data",
        implementation="""
    return {
        "cities": [
            {"name": "London", "country": "UK"},
            {"name": "New York", "country": "USA"},
            {"name": "Tokyo", "country": "Japan"},
            {"name": "Paris", "country": "France"},
            {"name": "Sydney", "country": "Australia"}
        ]
    }"""
    )
    
    add_resource(
        server_id="weather_service",
        uri="weather://{city}/alerts",
        name="Weather Alerts",
        description="Get weather alerts for a specific city",
        is_template=True,
        implementation="""
    # Simulated alerts
    alerts = {
        "london": ["Heavy rain expected tomorrow"],
        "tokyo": ["Typhoon warning in effect"]
    }
    
    city_lower = city.lower()
    return {
        "city": city,
        "alerts": alerts.get(city_lower, []),
        "last_updated": "2024-01-01T12:00:00Z"
    }"""
    )
    
    return {
        "success": True,
        "message": "Created example Weather Service server",
        "server_id": "weather_service",
        "preview": "Use 'generate_server_code' with server_id='weather_service' to see the generated code"
    }

# Resources
@mcp.resource("data://server-creator/info")
def get_creator_info() -> dict:
    """Provides information about the MCP Server Creator"""
    return {
        "name": "MCP Server Creator",
        "version": "1.0.0",
        "description": "A meta-MCP server that creates other MCP servers",
        "capabilities": [
            "Create server configurations",
            "Add tools with custom implementations",
            "Add static and dynamic resources",
            "Generate complete Python code",
            "Save servers to files"
        ],
        "servers_in_memory": len(servers)
    }

@mcp.resource("data://servers/{server_id}/code")
def get_server_code(server_id: str) -> dict:
    """Get the generated Python code for a specific server"""
    if server_id not in servers:
        return {"error": f"Server '{server_id}' not found"}
    
    return {
        "server_id": server_id,
        "name": servers[server_id].name,
        "code": generate_server_code(server_id)
    }


def main():
    """Entry point for the mcp-server-creator command"""
    mcp.run()

if __name__ == "__main__":
    main()
