import asyncio
import os

from dotenv import load_dotenv
from groq import Groq

from mcp import ClientSession
from mcp.client.stdio import (
    stdio_client,
    StdioServerParameters
)

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


async def generate_readme(project_folder):

    server_params = StdioServerParameters(
        command="cmd",
        args=[
            "/c",
            "npx",
            "-y",
            "@modelcontextprotocol/server-filesystem",
            project_folder
        ]
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            print("\nMCP Connected Successfully!\n")

            # -----------------------------
            # FIND PY FILES
            # -----------------------------
            search = await session.call_tool(
                "search_files",
                arguments={
                    "path": ".",
                    "pattern": "*.py"
                }
            )

            python_files = []

            for item in search.content:
                if hasattr(item, "text"):
                    for line in item.text.split("\n"):
                        line = line.strip().replace("[FILE]", "").strip()
                        if line.endswith(".py"):
                            python_files.append(line)

            python_files = list(set(python_files))

            print("\nPY FILES:", python_files)

            # -----------------------------
            # READ FILES
            # -----------------------------
            all_code = ""

            for file in python_files:

                print(f"READING: {file}")

                file_data = await session.call_tool(
                    "read_text_file",
                    arguments={
                        "path": file
                    }
                )

                file_text = ""

                for block in file_data.content:
                    if hasattr(block, "text"):
                        file_text += block.text

                all_code += f"\n\n===== {file} =====\n\n{file_text}"

            if not all_code.strip():
                print("\nNO CODE FOUND")
                return

            # -----------------------------
            # GROQ PROMPT
            # -----------------------------
            prompt = f"""
You are a senior software engineer.

Generate a professional README.md for this project.

Include:
- Title
- Description
- Features
- Installation
- Usage
- Project Structure

Return ONLY markdown.

CODE:
{all_code}
"""

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=3000
            )

            readme = response.choices[0].message.content

            print("\nREADME GENERATED\n")

            # -----------------------------
            # SAVE FILE (FIXED)
            # -----------------------------
            result = await session.call_tool(
                "write_file",
                arguments={
                    "path": "README.md",
                    "content": readme   # ✅ FIXED
                }
            )

            print("\nWRITE RESULT:", result)

            # -----------------------------
            # SAFETY BACKUP (IMPORTANT)
            # -----------------------------
            readme_path = os.path.join(project_folder, "README.md")

            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(readme)

            print("\nREADME SAVED (LOCAL + MCP)\n")
            print(readme)


async def main():

    folder = input("\nEnter Project Folder Path:\n").strip()

    if not os.path.exists(folder):
        print("Folder not found!")
        return

    await generate_readme(folder)


asyncio.run(main())