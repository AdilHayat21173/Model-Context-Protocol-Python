import asyncio
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession

async def main():
    print("🔌 Connecting to MCP Server...")

    async with streamablehttp_client("http://localhost:8000/mcp") as (read, write, _):
        async with ClientSession(read, write) as session:

            # Step 1: Initialize
            await session.initialize()
            print("✅ Connected!\n")

            # Step 2: List tools
            tools = await session.list_tools()
            print("🛠️  Available Tools:")
            for tool in tools.tools:
                print(f"   - {tool.name}: {tool.description}")

            print()

            # Step 3: Call ask_groq tool
            print("📨 Asking Groq a question...")
            result = await session.call_tool(
                "ask_groq",
                {"question": "What is Python in one line?"}
            )
            print("🤖 Groq says:", result.content[0].text)

asyncio.run(main())