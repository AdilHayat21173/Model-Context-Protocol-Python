from pathlib import Path
from docx import Document
from llm import ask_llm
import json

# ==============================
# DOCX FILE PATH
# ==============================

base_dir = Path(__file__).resolve().parent
file_name = base_dir / "Adil_Hayat_CV.docx"

# ==============================
# LOAD DOCX
# ==============================

doc = Document(file_name)

# ==============================
# EXTRACT CONTENT + STRUCTURE
# ==============================

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

    # Save full text
    full_text.append(text)

    # Detect headings
    if para.style.name.startswith("Heading"):
        cv_data["headings"].append(text)

    # Save paragraphs
    cv_data["paragraphs"].append({
        "text": text,
        "style": para.style.name
    })

cv_data["full_text"] = "\n".join(full_text)

# ==============================
# SHOW EXTRACTED DATA
# ==============================

print("\nEXTRACTED HEADINGS:")
print(cv_data["headings"])

print("\nFIRST 5 PARAGRAPHS:")

for p in cv_data["paragraphs"][:5]:
    print(p)

# ==============================
# CREATE PROMPT
# ==============================

prompt = f"""
You are an intelligent resume parser.

Analyze the resume and identify sections dynamically.

Instructions:
- Detect all resume sections automatically
- Extract content under each section
- Different resumes may have different section names
- Keep original section names if possible
- Return clean valid JSON only

Example sections may include:
- Summary
- Skills
- Experience
- Projects
- Education
- Certifications
- Achievements
- Languages
- Technical Skills
- Professional Profile
- Work History

Resume:

{cv_data['full_text']}
"""

# ==============================
# ASK LLM
# ==============================

result = ask_llm(prompt)

# ==============================
# PRINT RESPONSE
# ==============================

print("\nAI EXTRACTED DATA:\n")
print(result)

