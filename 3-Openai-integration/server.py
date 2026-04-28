import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from groq import Groq

# ✅ Load environment variables
load_dotenv()

# ✅ Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ✅ Create MCP Server
mcp = FastMCP("groq-mcp-server")


# ✅ Tool 1: Ask Groq a question
@mcp.tool()
def ask_groq(question: str) -> str:
    """Send a question to Groq LLM and get a response"""
    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content


# ✅ Tool 2: Summarize text using Groq
@mcp.tool()
def summarize_text(text: str) -> str:
    """Summarize any given text using Groq"""
    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "Summarize the following text briefly."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content


# ✅ Run server with Streamable HTTP transport
if __name__ == "__main__":
    print("🚀 MCP Server running at http://localhost:8000/mcp")
    mcp.run(transport="streamable-http")