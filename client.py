# client.py
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_cv_server():
    """Test the CV MCP server"""

    # Server parameters
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()

            print("🚀 Connected to CV MCP Server!")
            print("-" * 50)

            # List available resources
            resources = await session.list_resources()
            print("📂 Available Resources:")
            for resource in resources.resources:
                print(f"  - {resource.uri}: {resource.description}")

            print("\n🔧 Available Tools:")
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")

            print("\n" + "=" * 50)

            # Test getting CV content
            print("📄 Getting CV Summary:")
            cv_summary = await session.read_resource("file://cv/summary")
            print(cv_summary.contents[0].text[:200] + "...")

            print("\n🔍 Testing CV Search:")
            # Test search functionality
            search_result = await session.call_tool("search_cv", {"query": "experience"})
            print(f"Search for 'experience': {search_result.content[0].text}")

            print("\n❓ Testing CV Questions:")
            # Test question answering
            question_result = await session.call_tool("ask_about_cv", {"question": "What is my work experience?"})
            print(f"Question about work experience: {question_result.content[0].text}")

            print("\n📊 Getting CV Sections:")
            sections_result = await session.call_tool("get_cv_sections", {})
            print(f"CV sections info: {sections_result.content[0].text}")


if __name__ == "__main__":
    asyncio.run(test_cv_server())