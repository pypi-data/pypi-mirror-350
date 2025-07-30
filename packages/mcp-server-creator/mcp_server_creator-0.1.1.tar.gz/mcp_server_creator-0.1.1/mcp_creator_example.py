#!/usr/bin/env python3
"""
Example: Using the MCP Server Creator to build a Task Manager MCP Server
"""

import asyncio
from fastmcp import Client

async def create_and_explore():
    """Example of using the MCP Server Creator"""
    
    # Connect to the MCP Server Creator
    client = Client("mcp_server_creator_package.mcp_server_creator")
    
    async with client:
        print("🏗️  Connected to MCP Server Creator")
        
        # Step 1: Create a new server configuration
        print("\n📋 Creating Task Manager Server...")
        result = await client.call_tool("create_server", {
            "name": "Task Manager",
            "description": "An MCP server for managing tasks and to-do lists",
            "version": "1.0.0"
        })
        print(f"Result: {result[0].text}")
        
        # Step 2: Add tools to the server
        print("\n🔧 Adding tools...")
        
        # Add task creation tool (note the proper indentation in implementation)
        await client.call_tool("add_tool", {
            "server_id": "task_manager",
            "tool_name": "create_task",
            "description": "Create a new task",
            "parameters": [
                {"name": "title", "type": "str"},
                {"name": "description", "type": "str", "default": '""'},
                {"name": "priority", "type": "str", "default": '"medium"'},
                {"name": "due_date", "type": "str | None", "default": "None"}
            ],
            "return_type": "dict",
            "implementation": '''    import uuid
    from datetime import datetime
    
    task_id = str(uuid.uuid4())
    task = {
        "id": task_id,
        "title": title,
        "description": description,
        "priority": priority,
        "due_date": due_date,
        "created_at": datetime.now().isoformat(),
        "completed": False
    }
    
    # In a real implementation, save to database
    return {
        "success": True,
        "task": task,
        "message": f"Task '{title}' created successfully"
    }'''
        })
        
        # Add task listing tool
        await client.call_tool("add_tool", {
            "server_id": "task_manager",
            "tool_name": "list_tasks",
            "description": "List all tasks with optional filtering",
            "parameters": [
                {"name": "status", "type": "str | None", "default": "None"},
                {"name": "priority", "type": "str | None", "default": "None"}
            ],
            "return_type": "dict",
            "is_async": True,
            "implementation": '''    # Simulated task data
    tasks = [
        {
            "id": "1",
            "title": "Review MCP documentation",
            "priority": "high",
            "completed": False
        },
        {
            "id": "2", 
            "title": "Build example server",
            "priority": "medium",
            "completed": True
        }
    ]
    
    # Filter tasks
    filtered_tasks = tasks
    if status == "completed":
        filtered_tasks = [t for t in tasks if t["completed"]]
    elif status == "pending":
        filtered_tasks = [t for t in tasks if not t["completed"]]
    
    if priority:
        filtered_tasks = [t for t in filtered_tasks if t.get("priority") == priority]
    
    return {
        "total": len(filtered_tasks),
        "tasks": filtered_tasks
    }'''
        })
        
        # Add task completion tool
        await client.call_tool("add_tool", {
            "server_id": "task_manager",
            "tool_name": "complete_task",
            "description": "Mark a task as completed",
            "parameters": [
                {"name": "task_id", "type": "str"}
            ],
            "return_type": "dict",
            "implementation": '''    # In a real implementation, update in database
    return {
        "success": True,
        "task_id": task_id,
        "message": f"Task {task_id} marked as completed"
    }'''
        })
        
        # Step 3: Add resources
        print("\n📦 Adding resources...")
        
        # Add task statistics resource
        await client.call_tool("add_resource", {
            "server_id": "task_manager",
            "uri": "data://tasks/statistics",
            "name": "Task Statistics",
            "description": "Get statistics about all tasks",
            "implementation": '''    # Simulated statistics
    return {
        "total_tasks": 42,
        "completed": 28,
        "pending": 14,
        "by_priority": {
            "high": 5,
            "medium": 20,
            "low": 17
        },
        "completion_rate": "66.7%"
    }'''
        })
        
        # Add task detail resource template
        await client.call_tool("add_resource", {
            "server_id": "task_manager",
            "uri": "tasks://{task_id}/details",
            "name": "Task Details",
            "description": "Get detailed information about a specific task",
            "is_template": True,
            "implementation": '''    # Simulated task lookup
    task_data = {
        "1": {
            "id": "1",
            "title": "Review MCP documentation",
            "description": "Read through the FastMCP docs and examples",
            "priority": "high",
            "created_at": "2024-01-01T10:00:00Z",
            "due_date": "2024-01-05T17:00:00Z",
            "completed": False,
            "tags": ["documentation", "learning"]
        }
    }
    
    if task_id in task_data:
        return task_data[task_id]
    else:
        return {"error": f"Task {task_id} not found"}'''
        })
        
        # Step 4: Generate the server code
        print("\n🎯 Generating server code...")
        code_result = await client.call_tool("generate_server_code", {
            "server_id": "task_manager",
            "include_comments": True
        })
        
        print("\n📄 Generated code preview (first 50 lines):")
        print("=" * 60)
        lines = code_result[0].text.split('\n')
        for line in lines[:50]:
            print(line)
        print("... (truncated)")
        print("=" * 60)
        
        # Step 5: Save the server to a file
        print("\n💾 Saving server to file...")
        save_result = await client.call_tool("save_server", {
            "server_id": "task_manager",
            "filename": "task_manager_server.py"
        })
        print(f"Result: {save_result[0].text}")
        
        # Step 6: Get server details
        print("\n📊 Server details:")
        details = await client.call_tool("get_server_details", {
            "server_id": "task_manager"
        })
        print(details[0].text)
        
        # Step 7: Explore creator capabilities
        print("\n\n🔍 Exploring MCP Server Creator capabilities...")
        
        # Get creator info
        info = await client.read_resource("data://server-creator/info")
        print("\n📌 Server Creator Info:")
        print(info[0].text)
        
        # Create an example server
        print("\n🎨 Creating example server...")
        example_result = await client.call_tool("create_example_server", {})
        print(example_result[0].text)
        
        # List all servers
        print("\n📋 All servers in memory:")
        servers = await client.call_tool("list_servers", {})
        print(servers[0].text)
        
        # Get the example server code
        print("\n💻 Example server code:")
        code = await client.read_resource("data://servers/weather_service/code")
        print("First 30 lines of generated code:")
        code_data = eval(code[0].text)
        lines = code_data["code"].split('\n')
        for line in lines[:30]:
            print(line)

async def main():
    """Main example runner"""
    print("🚀 MCP Server Creator Example")
    print("=" * 60)
    
    # Run the complete example
    await create_and_explore()
    
    print("\n\n✅ Example completed!")
    print("\n📌 Next steps:")
    print("1. Run the generated server: fastmcp run task_manager_server.py")
    print("2. Test it with a client or Claude Desktop")
    print("3. Modify the generated code as needed")
    print("4. Create your own custom servers!")

if __name__ == "__main__":
    asyncio.run(main())
