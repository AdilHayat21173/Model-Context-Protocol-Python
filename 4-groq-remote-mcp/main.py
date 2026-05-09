import asyncio
import json
from dotenv import load_dotenv

load_dotenv()  # ✅ MUST be before Groq()

from groq import Groq
from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

# 1. MCP Server definition
MCP_SERVER = StdioServerParameters(
    command="npx",
    args=["-y", "@mzxrai/mcp-webresearch@latest"]
)

# 2. Groq client
client = Groq()


async def main():
    async with stdio_client(MCP_SERVER) as (read, write):
        async with ClientSession(read, write) as session:

            # 3. Initialize MCP
            await session.initialize()

            # 4. Get tools from MCP
            tools_result = await session.list_tools()

            # 5. Convert to Groq format (cleaned schema ✅)
            groq_tools = []
            for tool in tools_result.tools:
                schema = tool.inputSchema or {}
                clean_schema = {
                    "type": "object",
                    "properties": schema.get("properties", {}),
                    "required": schema.get("required", [])
                }
                groq_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": clean_schema
                    }
                })

            print("Tools loaded:", [t["function"]["name"] for t in groq_tools])

            # 6. First call — Groq decides which tool to use
            messages = [
                {"role": "user", "content": "Search the web for latest  news of pakistan and summarize it in 100 words."}
            ]

            response = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",  # ✅ tool-optimized model
                messages=messages,
                tools=groq_tools,
                tool_choice="auto",
                temperature=1,
                max_completion_tokens=1024,
                top_p=1,
                stream=False  # ⚠️ must be False when using tools
            )

            message = response.choices[0].message

            # 7. If Groq calls a tool → execute it via MCP
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)

                    print(f"\nCalling MCP tool: {tool_name}")
                    print(f"With args: {tool_args}")

                    # 8. MCP executes the tool
                    mcp_result = await session.call_tool(tool_name, tool_args)
                    tool_output = mcp_result.content[0].text

                    print(f"Tool result preview: {tool_output[:200]}...")

                    # 9. Send tool result back to Groq
                    messages.append({"role": "assistant", "tool_calls": [tool_call]})
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_output
                    })

            # 10. Final streaming response ✅
            completion = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",  # ✅ same model
                messages=messages,
                temperature=1,
                max_completion_tokens=1024,
                top_p=1,
                stream=True,
                stop=None
            )

            print("\n--- Final Answer ---")
            for chunk in completion:
                print(chunk.choices[0].delta.content or "", end="")


asyncio.run(main())