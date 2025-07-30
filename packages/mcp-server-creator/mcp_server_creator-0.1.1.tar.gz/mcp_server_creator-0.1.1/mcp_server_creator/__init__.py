"""
MCP Server Creator - A powerful Model Context Protocol (MCP) server that creates other MCP servers!

This meta-server provides tools for dynamically generating FastMCP server configurations and Python code.
"""

from .mcp_server_creator import mcp, main, create_server, add_tool, add_resource, generate_server_code

__version__ = "0.1.0"
__all__ = ["mcp", "main", "create_server", "add_tool", "add_resource", "generate_server_code"]
