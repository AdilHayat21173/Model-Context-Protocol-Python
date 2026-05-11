from llm import ask_llm


# ==============================
# GENERATE EMAIL
# ==============================

def generate_application_email(cv_data: dict, job_description: str) -> dict:
    """
    Takes cv_data (from content.py) and a job description string.
    Returns a dict with:
        - subject   : email subject line
        - body      : full email body
    """

    prompt = f"""
You are a professional career coach and email writer.

Write a job application email based on the CV and job description below.

Instructions:
- Tone: Professional, confident, and enthusiastic
- Length: Medium (not too short, not too long — 4 to 5 paragraphs)
- Do NOT use generic filler phrases like "I hope this email finds you well"
- Do NOT repeat the entire CV — highlight only the most relevant skills and projects
- Mention 2–3 specific projects or achievements from the CV that match the job
- End with a clear call to action (e.g. request for interview)
- Output ONLY two things, clearly separated:

SUBJECT: <your subject line here>

BODY:
<your email body here>

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

        # Extract subject line
        if stripped.upper().startswith("SUBJECT:"):
            subject = stripped[len("SUBJECT:"):].strip()
            continue

        # Start collecting body
        if stripped.upper().startswith("BODY:"):
            in_body = True
            # Grab anything after "BODY:" on the same line
            after = stripped[len("BODY:"):].strip()
            if after:
                body_lines.append(after)
            continue

        if in_body:
            body_lines.append(line)

    body = "\n".join(body_lines).strip()

    # Fallback: if parsing failed, return full response as body
    if not body:
        body = response.strip()
    if not subject:
        subject = "Application for AI/ML Engineer Position"

    return {
        "subject": subject,
        "body": body
    }


# ==============================
# SAVE EMAIL TO .TXT FILE
# ==============================

def save_email(email: dict, output_path: str = "application_email.txt"):
    """
    Save the generated email to a .txt file.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"SUBJECT: {email['subject']}\n")
        f.write("=" * 60 + "\n\n")
        f.write(email["body"])

    print(f"\nEmail saved to: {output_path}")


# ==============================
# PRINT EMAIL TO CONSOLE
# ==============================

def print_email(email: dict):
    print("\n" + "=" * 60)
    print("GENERATED APPLICATION EMAIL")
    print("=" * 60)
    print(f"\nSUBJECT: {email['subject']}\n")
    print("-" * 60)
    print(email["body"])
    print("=" * 60)