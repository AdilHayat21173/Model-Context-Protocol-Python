from llm import ask_llm


# ==============================
# GENERATE EMAIL
# ==============================

def generate_application_email(cv_data: dict, job_description: str) -> dict:
    """
    Takes cv_data (from content.py) and a job description string.
    Returns:
        {
            "subject": "...",
            "body": "..."
        }
    """

    prompt = f"""
You are a professional job application email writer.

Write a simple and natural job application email based on the CV and job description.

Very important rules:
- Do NOT write long paragraphs
- Do NOT use phrases like "seasoned", "proven track record", "cutting-edge", "align perfectly"
- Do NOT overpraise the candidate
- Do NOT mention too many projects
- Mention only 1 or 2 relevant skills/projects
- Keep the email short and human-like
- Maximum 180 words
- Use simple English
- Start exactly with: Hello,
- Mention the job title
- Mention company name only if available
- Mention that the CV/resume is attached
- End exactly like this:

Thanks,
{cv_data.get('name', 'Adil Hayat')}

Output ONLY in this format:

SUBJECT: <subject line>

BODY:
<email body>

CV:
{cv_data['full_text']}

Job Description:
{job_description}
"""

    response = ask_llm(prompt)

    return parse_email(response)


# ==============================
# PARSE SUBJECT + BODY
# ==============================

def parse_email(response: str) -> dict:
    """
    Parse the LLM response into subject and body.

    Expected format:

    SUBJECT: ...

    BODY:
    ...
    """

    subject = ""
    body_lines = []
    in_body = False

    for line in response.splitlines():
        stripped = line.strip()

        # Extract subject
        if stripped.upper().startswith("SUBJECT:"):
            subject = stripped[len("SUBJECT:"):].strip()
            continue

        # Start body parsing
        if stripped.upper().startswith("BODY:"):
            in_body = True

            # Capture inline content after BODY:
            after = stripped[len("BODY:"):].strip()
            if after:
                body_lines.append(after)

            continue

        if in_body:
            body_lines.append(line)

    body = "\n".join(body_lines).strip()

    # Fallbacks
    if not subject:
        subject = "Application for AI/ML Engineer Position"

    if not body:
        body = response.strip()

    return {
        "subject": subject,
        "body": body
    }


# ==============================
# SAVE EMAIL TO FILE
# ==============================

def save_email(email: dict, output_path: str = "application_email.txt"):
    """
    Save generated email to a text file.
    """

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"SUBJECT: {email['subject']}\n")
        f.write("=" * 60 + "\n\n")
        f.write(email["body"])

    print(f"\n✅ Email saved to: {output_path}")


# ==============================
# PRINT EMAIL
# ==============================

def print_email(email: dict):
    """
    Print formatted email in console.
    """

    print("\n" + "=" * 60)
    print("GENERATED APPLICATION EMAIL")
    print("=" * 60)

    print(f"\nSUBJECT: {email['subject']}\n")

    print("-" * 60)

    print(email["body"])

    print("\n" + "=" * 60)

