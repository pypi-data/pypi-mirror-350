#!/usr/bin/env python3
"""
Test script for SaasToMCP server.
This demonstrates how to use the server to register APIs and call their endpoints.
"""

import asyncio
import json
import sys
import os
from pathlib import Path

# Add src to path for development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fastmcp import Client


async def main():
    print("🧪 Testing SaasToMCP Server\n")
    
    # Connect to the SaasToMCP server using the main entry point
    client = Client("main.py")
    
    try:
        async with client:
            print("✅ Connected to SaasToMCP server")
            
            # List available tools
            tools = await client.list_tools()
            print(f"🔧 Available tools: {[t.name for t in tools]}\n")
            
            # Load and register the JSONPlaceholder API (no auth required)
            config_path = Path("examples/jsonplaceholder_api.json")
            if not config_path.exists():
                print(f"❌ Configuration file not found: {config_path}")
                print("Please make sure you're running this from the project root directory.")
                return
            
            with open(config_path, "r") as f:
                api_config = json.load(f)
            
            print("1️⃣ Registering JSONPlaceholder API...")
            result = await client.call_tool("register_api", {"config": api_config})
            print(f"   ✅ {result[0].text}\n")
            
            # List registered APIs
            print("2️⃣ Listing registered APIs...")
            apis = await client.list_apis()
            print(f"   📋 Registered APIs:")
            for api_name, api_info in apis[0].text.items():
                print(f"      • {api_name}: {api_info['base_url']}")
                for endpoint in api_info['endpoints']:
                    print(f"        - {endpoint['method']} {endpoint['path']} ({endpoint['name']})")
            print()
            
            # Test the API connection
            print("3️⃣ Testing API connection...")
            test_result = await client.call_tool("test_api_connection", {"api_name": "jsonplaceholder"})
            status = test_result[0].text
            print(f"   🔍 Connection status: {status['status']}")
            if status['status'] == 'connected':
                print(f"   📡 HTTP Status: {status['status_code']}")
            else:
                print(f"   ❌ Error: {status.get('error', 'Unknown error')}")
            print()
            
            # Call an endpoint - List posts
            print("4️⃣ Calling API endpoint - List posts...")
            try:
                posts = await client.call_tool("call_api_endpoint", {
                    "api_name": "jsonplaceholder",
                    "endpoint_name": "list_posts",
                    "parameters": {"_limit": 3}
                })
                posts_data = posts[0].text
                print(f"   📝 Retrieved {len(posts_data)} posts:")
                for i, post in enumerate(posts_data[:2]):  # Show first 2
                    print(f"      {i+1}. {post['title'][:50]}...")
                print()
            except Exception as e:
                print(f"   ❌ Error calling endpoint: {e}\n")
            
            # Call another endpoint - Get specific post
            print("5️⃣ Getting specific post...")
            try:
                post = await client.call_tool("call_api_endpoint", {
                    "api_name": "jsonplaceholder",
                    "endpoint_name": "get_post",
                    "parameters": {"id": 1}
                })
                post_data = post[0].text
                print(f"   📄 Post 1: '{post_data['title']}'")
                print(f"      👤 User ID: {post_data['userId']}")
                print(f"      📝 Body: {post_data['body'][:100]}...")
                print()
            except Exception as e:
                print(f"   ❌ Error getting post: {e}\n")
            
            # Create a new post
            print("6️⃣ Creating a new post...")
            try:
                new_post = await client.call_tool("call_api_endpoint", {
                    "api_name": "jsonplaceholder",
                    "endpoint_name": "create_post",
                    "parameters": {
                        "title": "Test Post from SaasToMCP",
                        "body": "This is a test post created using the SaasToMCP server!",
                        "userId": 1
                    }
                })
                created_post = new_post[0].text
                print(f"   ✅ Created post with ID: {created_post['id']}")
                print(f"      📝 Title: {created_post['title']}")
                print()
            except Exception as e:
                print(f"   ❌ Error creating post: {e}\n")
            
            # Unregister the API
            print("7️⃣ Unregistering API...")
            try:
                unregister_result = await client.call_tool("unregister_api", {"api_name": "jsonplaceholder"})
                print(f"   ✅ {unregister_result[0].text}")
            except Exception as e:
                print(f"   ❌ Error unregistering API: {e}")
            
            print("\n🎉 Test completed successfully!")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
