#!/usr/bin/env python3
"""
SaasToMCP Server Entry Point

This script provides backward compatibility and a simple way to run the server.
"""

import sys
import os

# Add the src directory to Python path for development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from saas_to_mcp.server import SaasToMCP


def main():
    """Run the SaasToMCP server."""
    server = SaasToMCP()
    
    try:
        print("🚀 Starting SaasToMCP server...")
        print("📝 Use the register_api tool to add your APIs")
        print("🔧 Available core tools: register_api, list_apis, call_api_endpoint, unregister_api, test_api_connection")
        print("⌨️  Press Ctrl+C to stop\n")
        
        server.run()
    except KeyboardInterrupt:
        print("\n👋 Shutting down server...")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
