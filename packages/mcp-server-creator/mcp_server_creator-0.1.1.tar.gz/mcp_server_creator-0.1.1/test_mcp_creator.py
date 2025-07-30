#!/usr/bin/env python3
"""
Test script for MCP Server Creator
Run this to verify that the MCP Server Creator is working correctly
"""

import asyncio
import json
from fastmcp import Client

async def test_all_features():
    """Test all MCP Server Creator functionality in a single connection"""
    
    print("🧪 Testing MCP Server Creator\n")
    
    # Connect to the MCP Server Creator
    client = Client("mcp_server_creator_package.mcp_server_creator")
    
    async with client:
        # Test 1: Create a server
        print("Test 1: Creating a test server...")
        result = await client.call_tool("create_server", {
            "name": "Test Server",
            "description": "A test server for validation",
            "version": "0.1.0"
        })
        result_data = json.loads(result[0].text)
        assert result_data["success"] == True
        print("✅ Server creation successful")
        
        # Test 2: Add a simple tool
        print("\nTest 2: Adding a simple tool...")
        result = await client.call_tool("add_tool", {
            "server_id": "test_server",
            "tool_name": "echo",
            "description": "Echo back the input",
            "parameters": [{"name": "message", "type": "str"}],
            "return_type": "str",
            "implementation": "    return f'Echo: {message}'"
        })
        result_data = json.loads(result[0].text)
        assert result_data["success"] == True
        print("✅ Tool addition successful")
        
        # Test 3: Add an async tool
        print("\nTest 3: Adding an async tool...")
        result = await client.call_tool("add_tool", {
            "server_id": "test_server",
            "tool_name": "delayed_response",
            "description": "Respond after a delay",
            "parameters": [
                {"name": "message", "type": "str"},
                {"name": "delay", "type": "float", "default": "1.0"}
            ],
            "return_type": "dict",
            "is_async": True,
            "implementation": """    import asyncio
    await asyncio.sleep(delay)
    return {
        "message": message,
        "delayed_by": delay,
        "timestamp": str(asyncio.get_event_loop().time())
    }"""
        })
        result_data = json.loads(result[0].text)
        assert result_data["success"] == True
        print("✅ Async tool addition successful")
        
        # Test 4: Add a resource
        print("\nTest 4: Adding a static resource...")
        result = await client.call_tool("add_resource", {
            "server_id": "test_server",
            "uri": "data://test/info",
            "name": "Test Information",
            "description": "Static test information",
            "implementation": """    return {
        "name": "Test Server",
        "status": "operational",
        "test_data": [1, 2, 3, 4, 5]
    }"""
        })
        result_data = json.loads(result[0].text)
        assert result_data["success"] == True
        print("✅ Resource addition successful")
        
        # Test 5: Add a resource template
        print("\nTest 5: Adding a resource template...")
        result = await client.call_tool("add_resource", {
            "server_id": "test_server",
            "uri": "test://{item_id}/details",
            "name": "Item Details",
            "description": "Get details for a specific item",
            "is_template": True,
            "implementation": """    items = {
        "item1": {"name": "First Item", "value": 100},
        "item2": {"name": "Second Item", "value": 200}
    }
    return items.get(item_id, {"error": f"Item {item_id} not found"})"""
        })
        result_data = json.loads(result[0].text)
        assert result_data["success"] == True
        print("✅ Resource template addition successful")
        
        # Test 6: List servers
        print("\nTest 6: Listing all servers...")
        result = await client.call_tool("list_servers", {})
        servers = json.loads(result[0].text)
        assert len(servers) >= 1
        assert any(s["server_id"] == "test_server" for s in servers)
        print(f"✅ Found {len(servers)} server(s)")
        
        # Test 7: Get server details
        print("\nTest 7: Getting server details...")
        result = await client.call_tool("get_server_details", {
            "server_id": "test_server"
        })
        details = json.loads(result[0].text)
        assert details["server_id"] == "test_server"
        assert len(details["tools"]) == 2
        assert len(details["resources"]) == 2
        print("✅ Server details retrieved successfully")
        
        # Test 8: Generate code
        print("\nTest 8: Generating server code...")
        result = await client.call_tool("generate_server_code", {
            "server_id": "test_server",
            "include_comments": True
        })
        code = result[0].text
        assert "FastMCP" in code
        assert "def echo" in code
        assert "async def delayed_response" in code
        assert "@mcp.resource" in code
        print("✅ Code generation successful")
        lines_count = len(code.split('\n'))
        print(f"   Generated {lines_count} lines of code")
        
        # Test 9: Check resources
        print("\nTest 9: Checking resources...")
        
        # Check creator info
        info = await client.read_resource("data://server-creator/info")
        info_data = json.loads(info[0].text)
        assert "capabilities" in info_data
        print("✅ Creator info resource accessible")
        
        # Check generated code resource
        code_resource = await client.read_resource("data://servers/test_server/code")
        code_data = json.loads(code_resource[0].text)
        assert code_data["server_id"] == "test_server"
        assert "code" in code_data
        print("✅ Server code resource accessible")
        
        # Test 10: Error handling
        print("\nTest 10: Testing error handling...")
        
        # Try to create duplicate server
        result = await client.call_tool("create_server", {
            "name": "Test Server",
            "description": "Duplicate test"
        })
        result_data = json.loads(result[0].text)
        assert result_data["success"] == False
        assert "already exists" in result_data["error"]
        print("✅ Duplicate server error handled correctly")
        
        # Try to add tool to non-existent server
        result = await client.call_tool("add_tool", {
            "server_id": "non_existent",
            "tool_name": "test",
            "description": "Test",
            "parameters": []
        })
        result_data = json.loads(result[0].text)
        assert result_data["success"] == False
        assert "not found" in result_data["error"]
        print("✅ Non-existent server error handled correctly")
        
        print("\n🎉 All basic tests passed!")
        
        # Test 11: Create and test example server
        print("\n\n🎨 Testing Example Server Creation\n")
        
        # Create the example server
        print("Creating example Weather Service...")
        result = await client.call_tool("create_example_server", {})
        result_data = json.loads(result[0].text)
        assert result_data["success"] == True
        print("✅ Example server created successfully")
        
        # Check the example server details
        result = await client.call_tool("get_server_details", {
            "server_id": "weather_service"
        })
        details = json.loads(result[0].text)
        print(f"\n📊 Weather Service Details:")
        print(f"   Tools: {len(details['tools'])}")
        for tool in details['tools']:
            print(f"     - {tool['name']}: {tool['description']}")
        print(f"   Resources: {len(details['resources'])}")
        for resource in details['resources']:
            print(f"     - {resource['uri']}: {resource['name']}")
        
        # Test 12: Save the test server
        print("\n\n💾 Saving test server to file...")
        result = await client.call_tool("save_server", {
            "server_id": "test_server",
            "filename": "test_server_output.py"
        })
        save_data = json.loads(result[0].text)
        if save_data["success"]:
            print(f"✅ Test server saved to: {save_data['path']}")
            print(f"   File size: {save_data['size']} bytes")
        
        # Test 13: Generate and preview weather service code
        print("\n\n💻 Weather Service generated code preview:")
        result = await client.call_tool("generate_server_code", {
            "server_id": "weather_service"
        })
        code = result[0].text
        print("First 30 lines of generated code:")
        print("=" * 60)
        lines = code.split('\n')
        for line in lines[:30]:
            print(line)
        print("... (truncated)")
        print("=" * 60)
        
        return True

async def main():
    """Run all tests"""
    try:
        # Run all tests in a single connection
        await test_all_features()
        
        print("\n\n✅ All tests completed successfully!")
        print("\n📌 Next steps:")
        print("1. Check the generated 'test_server_output.py' file")
        print("2. Run it with: fastmcp run test_server_output.py")
        print("3. Create your own custom servers!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    asyncio.run(main())
