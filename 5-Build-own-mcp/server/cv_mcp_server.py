from mcp.server.fastmcp import FastMCP
from pathlib import Path
from docx import Document
import sys

# Add server directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from job_analyzer import extract_job_requirements, suggest_cv_updates as _suggest
from docx_updater import update_cv_docx as _update_docx
from email_generator import generate_application_email as _gen_email

mcp = FastMCP("cv-automation")


@mcp.tool()
def load_cv(cv_path: str) -> dict:
    """
    Load a CV .docx file and return structured CV data.
    """
    doc_path = Path(cv_path)

    if not doc_path.exists():
        raise FileNotFoundError(f"CV file not found: {cv_path}")

    if doc_path.suffix.lower() != ".docx":
        raise ValueError("Only .docx files are supported.")

    doc = Document(str(doc_path))

    cv_data = {
        "headings": [],
        "paragraphs": [],
        "full_text": ""
    }

    full_text = []

    for para in doc.paragraphs:
        text = para.text.strip()

        if not text:
            continue

        full_text.append(text)

        if para.style.name.startswith("Heading"):
            cv_data["headings"].append(text)

        cv_data["paragraphs"].append({
            "text": text,
            "style": para.style.name
        })

    cv_data["full_text"] = "\n".join(full_text)

    return cv_data


@mcp.tool()
def analyze_job_description(job_description: str) -> dict:
    """
    Extract required skills, tools, ATS keywords, and job requirements
    from the job description.
    """
    if not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    return extract_job_requirements(job_description)


@mcp.tool()
def suggest_cv_updates(cv_full_text: str, job_data: dict) -> str:
    """
    Compare CV text with job requirements and return updated Technical Skills.
    """
    if not cv_full_text.strip():
        raise ValueError("CV text cannot be empty.")

    if not isinstance(job_data, dict):
        raise ValueError("job_data must be a dictionary.")

    cv_data = {
        "full_text": cv_full_text
    }

    suggestions = _suggest(cv_data, job_data)

    if not suggestions or not suggestions.strip():
        raise ValueError("No CV suggestions were generated.")

    return suggestions


@mcp.tool()
def update_cv_docx(cv_path: str, suggestions: str, output_path: str) -> str:
    """
    Replace the Technical Skills section in the CV .docx file.
    """
    if not suggestions.strip():
        raise ValueError("Suggestions cannot be empty.")

    if "Error executing tool" in suggestions or "validation error" in suggestions.lower():
        raise ValueError("Suggestions contain an error message. CV update stopped.")

    input_path = Path(cv_path)

    if not input_path.exists():
        raise FileNotFoundError(f"CV file not found: {cv_path}")

    saved_path = _update_docx(
        cv_path=cv_path,
        suggestions=suggestions,
        output_path=output_path
    )

    return saved_path


@mcp.tool()
def generate_application_email(cv_full_text: str, job_description: str) -> dict:
    """
    Generate a professional job application email based on CV and JD.
    """
    if not cv_full_text.strip():
        raise ValueError("CV text cannot be empty.")

    if not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    cv_data = {
        "full_text": cv_full_text
    }

    return _gen_email(cv_data, job_description)


if __name__ == "__main__":
    mcp.run()