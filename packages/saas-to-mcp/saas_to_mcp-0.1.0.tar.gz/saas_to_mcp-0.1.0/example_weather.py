#!/usr/bin/env python3
"""
Example: Using SaasToMCP with a real API.
This example shows how to configure and use the OpenWeatherMap API.
"""

import asyncio
import json
from fastmcp import Client


# Example API configuration for OpenWeatherMap
WEATHER_API_CONFIG = {
    "name": "weather",
    "base_url": "https://api.openweathermap.org/data/2.5",
    "description": "OpenWeatherMap API",
    "auth": {
        "type": "api_key",
        "api_key": "YOUR_API_KEY_HERE",  # Replace with your actual API key
        "api_key_param": "appid"
    },
    "endpoints": [
        {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "method": "GET",
            "path": "/weather",
            "params": [
                {
                    "name": "q",
                    "type": "string",
                    "location": "query",
                    "required": True,
                    "description": "City name"
                },
                {
                    "name": "units",
                    "type": "string",
                    "location": "query",
                    "required": False,
                    "default": "metric",
                    "enum": ["metric", "imperial", "kelvin"],
                    "description": "Units of measurement"
                }
            ]
        }
    ]
}


async def main():
    # Connect to the SaasToMCP server
    client = Client("saas_to_mcp.py")
    
    async with client:
        print("Connected to SaasToMCP server\n")
        
        # Check if you've set your API key
        if WEATHER_API_CONFIG["auth"]["api_key"] == "YOUR_API_KEY_HERE":
            print("⚠️  Please set your OpenWeatherMap API key in the WEATHER_API_CONFIG")
            print("   You can get a free API key at: https://openweathermap.org/api")
            print("\nFor this demo, we'll use the JSONPlaceholder API instead...\n")
            
            # Use JSONPlaceholder API for demo
            with open("examples/jsonplaceholder_api.json", "r") as f:
                api_config = json.load(f)
            
            # Register the API
            result = await client.call_tool("register_api", {"config": api_config})
            print(f"✅ Registered API: {result[0].text}")
            
            # List posts
            posts = await client.call_tool("jsonplaceholder_list_posts", {"_limit": 2})
            print(f"\n📝 Sample posts:")
            print(json.dumps(posts[0].text, indent=2))
            
        else:
            # Register the Weather API
            print("1. Registering Weather API...")
            result = await client.call_tool("register_api", {"config": WEATHER_API_CONFIG})
            print(f"   ✅ {result[0].text}")
            
            # Test the connection
            print("\n2. Testing API connection...")
            test = await client.call_tool("test_api_connection", {"api_name": "weather"})
            print(f"   Status: {test[0].text['status']}")
            
            # Get weather for a city
            print("\n3. Getting weather for London...")
            weather = await client.call_tool("weather_get_weather", {
                "q": "London",
                "units": "metric"
            })
            
            data = weather[0].text
            print(f"\n🌤️  Weather in {data['name']}, {data['sys']['country']}:")
            print(f"   Temperature: {data['main']['temp']}°C")
            print(f"   Feels like: {data['main']['feels_like']}°C")
            print(f"   Conditions: {data['weather'][0]['description']}")
            print(f"   Humidity: {data['main']['humidity']}%")
            print(f"   Wind: {data['wind']['speed']} m/s")
            
            # Try another city
            print("\n4. Getting weather for New York...")
            weather = await client.call_tool("weather_get_weather", {
                "q": "New York",
                "units": "imperial"
            })
            
            data = weather[0].text
            print(f"\n🌤️  Weather in {data['name']}, {data['sys']['country']}:")
            print(f"   Temperature: {data['main']['temp']}°F")
            print(f"   Conditions: {data['weather'][0]['description']}")


if __name__ == "__main__":
    asyncio.run(main())
