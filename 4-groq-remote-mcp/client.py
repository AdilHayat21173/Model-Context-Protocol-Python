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
You are a senior software engineer writing professional GitHub documentation.

STRICT RULES:
- Only use information that is explicitly present in the code.
- Do NOT assume, invent, or hallucinate any features, files, or architecture.
- If something is not in the code, do NOT mention it.

---

# TASK
Generate a professional README.md for the project.

---

# REQUIRED SECTIONS

## 1. Project Title
Derive from actual code context only.

## 2. Project Description
Explain exactly what the code does.

## 3. Project Overview (VERY IMPORTANT)
This project contains ONLY:
- main.py
- client.py

Explain each file’s real responsibility:
- main.py → MCP + Groq tool calling + web search agent
- client.py → MCP filesystem reader + README generator using Groq

Explain how they work independently (NOT a combined system unless explicitly connected in code).

---

## 4. Execution Flow (REAL FLOW ONLY)
Describe step-by-step execution based on actual logic:
- What main.py does when run
- What client.py does when run
- Do NOT merge them into one pipeline unless code connects them

---

## 5. File-by-File Breakdown
Explain each file:
- Purpose
- Main functions
- Real behavior only

---

## 6. Features (FROM CODE ONLY)
List only what exists:
- MCP filesystem usage
- Groq LLM usage
- Web search tool (if present in code)
- README generation (client.py)

---

## 7. Technologies Used
Only actual dependencies:
- Python
- Groq API
- MCP
- asyncio

---

## 8. Installation
Simple and realistic setup steps.

---

## 9. Usage
Explain:
- how to run main.py
- how to run client.py

---

## 10. Project Structure
Only real files:

project/
├── main.py
├── client.py
├── README.md
├── .env

---

# OUTPUT RULES
- Return ONLY markdown
- No extra explanation
- No assumptions
- No invented components
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