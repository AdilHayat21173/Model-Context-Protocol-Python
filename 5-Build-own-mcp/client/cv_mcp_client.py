"""
CLI client for CV Automation MCP pipeline.

Run from main project folder:

python client/cv_mcp_client.py --cv "Adil_Hayat_CV.docx" --jd "paste job description here"
"""

import asyncio
import json
import argparse
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# Fix Windows terminal Unicode printing issue
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def clean_text_for_docx(text: str) -> str:
    """
    Replace special Unicode characters that can cause Windows charmap errors.
    """
    if not text:
        return ""

    replacements = {
        "\u2011": "-",   # non-breaking hyphen
        "\u2010": "-",   # hyphen
        "\u2012": "-",   # figure dash
        "\u2013": "-",   # en dash
        "\u2014": "-",   # em dash
        "\u2018": "'",   # left single quote
        "\u2019": "'",   # right single quote
        "\u201c": '"',   # left double quote
        "\u201d": '"',   # right double quote
        "\u2022": "-",   # bullet
        "\u00a0": " ",   # non-breaking space
        "\ufeff": "",    # BOM
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


def get_tool_text(result) -> str:
    """
    Safely extract text from MCP tool result.
    """
    if not result.content:
        return ""

    return result.content[0].text


def has_tool_error(text: str) -> bool:
    """
    Detect tool errors before passing output to the next tool.
    """
    if not text:
        return False

    error_keywords = [
        "Error executing tool",
        "validation error",
        "Traceback",
        "Exception",
        "FileNotFoundError",
        "ValueError",
        "charmap codec",
        "codec can't encode",
    ]

    text_lower = text.lower()

    return any(keyword.lower() in text_lower for keyword in error_keywords)


async def run_pipeline(cv_path: str, job_description: str):
    """
    Run full CV automation flow:
    1. Load CV
    2. Analyze JD
    3. Suggest CV skill updates
    4. Update DOCX CV
    5. Generate application email
    """

    cv_file = Path(cv_path)

    if not cv_file.exists():
        print(f"CV file not found: {cv_path}")
        return

    if cv_file.suffix.lower() != ".docx":
        print("Only .docx CV files are supported.")
        return

    if not job_description.strip():
        print("Job description cannot be empty.")
        return

    server_params = StdioServerParameters(
        command="python",
        args=["server/cv_mcp_server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # STEP 1: Load CV
            print("\n=== STEP 1: Load CV ===")

            cv_result = await session.call_tool(
                "load_cv",
                {
                    "cv_path": str(cv_file)
                }
            )

            cv_text_result = get_tool_text(cv_result)

            if has_tool_error(cv_text_result):
                print("load_cv tool failed:")
                print(cv_text_result)
                return

            try:
                cv_data = json.loads(cv_text_result)
            except Exception as e:
                print("Could not parse CV data from MCP response.")
                print(e)
                print(cv_text_result)
                return

            cv_text = cv_data.get("full_text", "")

            if not cv_text.strip():
                print("CV loaded, but full_text is empty.")
                return

            print(f"CV loaded successfully. Characters: {len(cv_text)}")

            # STEP 2: Analyze Job Description
            print("\n=== STEP 2: Analyze Job Description ===")

            jd_result = await session.call_tool(
                "analyze_job_description",
                {
                    "job_description": job_description
                }
            )

            jd_text_result = get_tool_text(jd_result)

            if has_tool_error(jd_text_result):
                print("analyze_job_description tool failed:")
                print(jd_text_result)
                return

            try:
                job_data = json.loads(jd_text_result)
            except Exception as e:
                print("Could not parse job analysis data from MCP response.")
                print(e)
                print(jd_text_result)
                return

            print("Job description analyzed successfully.")
            print(json.dumps(job_data, indent=2, ensure_ascii=False))

            # STEP 3: Suggest CV Updates
            print("\n=== STEP 3: Suggest CV Updates ===")

            skills_result = await session.call_tool(
                "suggest_cv_updates",
                {
                    "cv_full_text": cv_text,
                    "job_data": job_data
                }
            )

            suggestions = get_tool_text(skills_result)
            suggestions = clean_text_for_docx(suggestions)

            if has_tool_error(suggestions):
                print("suggest_cv_updates tool failed. CV will NOT be updated.")
                print(suggestions)
                return

            if not suggestions.strip():
                print("No skill suggestions generated. CV will NOT be updated.")
                return

            print("Skill suggestions generated successfully:")
            print(suggestions)

            # STEP 4: Update CV DOCX
            print("\n=== STEP 4: Update CV DOCX ===")

            output_path = str(cv_file.with_name(cv_file.stem + "_updated.docx"))

            update_result = await session.call_tool(
                "update_cv_docx",
                {
                    "cv_path": str(cv_file),
                    "suggestions": suggestions,
                    "output_path": output_path
                }
            )

            updated_cv_path = get_tool_text(update_result)
            updated_cv_path = clean_text_for_docx(updated_cv_path)

            if has_tool_error(updated_cv_path):
                print("update_cv_docx tool failed:")
                print(updated_cv_path)
                return

            print(f"Updated CV saved at: {updated_cv_path}")

            # STEP 5: Generate Application Email
            print("\n=== STEP 5: Generate Application Email ===")

            email_result = await session.call_tool(
                "generate_application_email",
                {
                    "cv_full_text": cv_text,
                    "job_description": job_description
                }
            )

            email_text_result = get_tool_text(email_result)
            email_text_result = clean_text_for_docx(email_text_result)

            if has_tool_error(email_text_result):
                print("generate_application_email tool failed:")
                print(email_text_result)
                return

            try:
                email = json.loads(email_text_result)
            except Exception:
                print("Email generated, but response is not JSON. Raw response:")
                print(email_text_result)
                return

            subject = clean_text_for_docx(email.get("subject", ""))
            body = clean_text_for_docx(email.get("body", ""))

            print("\nApplication Email")
            print("-----------------")
            print("Subject:", subject)
            print()
            print(body)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CV Automation MCP Client")

    parser.add_argument(
        "--cv",
        required=True,
        help="Path to CV .docx file"
    )

    parser.add_argument(
        "--jd",
        required=True,
        help="Job description text"
    )

    args = parser.parse_args()

    asyncio.run(run_pipeline(args.cv, args.jd))