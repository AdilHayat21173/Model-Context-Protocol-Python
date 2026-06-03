# CV Automation MCP Server

A Model Context Protocol (MCP) server that helps automate resume optimization for job applications. The server can load CVs, analyze job descriptions, identify missing skills, update resumes, and generate professional application emails using AI.

## Features

### Load CV

Reads a DOCX resume and extracts:

* Full CV text
* Headings
* Paragraphs
* Document structure

### Analyze Job Description

Extracts:

* Required skills
* Technologies
* ATS keywords
* Job requirements

### Suggest CV Updates

Compares a CV against a job description and:

* Identifies missing skills
* Suggests ATS-friendly keywords
* Recommends improvements for the Technical Skills section

### Update CV Document

Automatically updates the Technical Skills section of a DOCX resume and saves an updated version.

### Generate Application Email

Creates a professional job application email tailored to a specific job description.

---

## Project Structure

```text
.
├── client/
│   └── cv_mcp_client.py
│
├── server/
│   ├── cv_mcp_server.py
│   ├── job_analyzer.py
│   ├── docx_updater.py
│   ├── email_generator.py
│   ├── llm.py
│   └── content.py
│
├── Adil_Hayat_CV.docx
├── Adil_Hayat_CV_updated.docx
└── main.py
```

---

## MCP Tools

### load_cv

Loads a DOCX resume and extracts structured CV data.

**Input**

```python
load_cv(cv_path="Adil_Hayat_CV.docx")
```

---

### analyze_job_description

Analyzes a job description and extracts skills, tools, ATS keywords, and requirements.

**Input**

```python
analyze_job_description(
    job_description="Job description text"
)
```

---

### suggest_cv_updates

Compares CV content with job requirements and generates updated Technical Skills suggestions.

**Input**

```python
suggest_cv_updates(
    cv_full_text="CV content",
    job_data=job_requirements
)
```

---

### update_cv_docx

Updates the Technical Skills section of a DOCX resume and saves a new version.

**Input**

```python
update_cv_docx(
    cv_path="Adil_Hayat_CV.docx",
    suggestions="Updated skills",
    output_path="Adil_Hayat_CV_updated.docx"
)
```

---

### generate_application_email

Generates a professional application email based on the candidate's CV and job description.

**Input**

```python
generate_application_email(
    cv_full_text="CV content",
    job_description="Job description"
)
```

---

## Workflow

```text
Load CV
   ↓
Analyze Job Description
   ↓
Compare CV with JD
   ↓
Generate Skill Suggestions
   ↓
Update CV
   ↓
Generate Application Email
```

---

## Use Cases

* Resume optimization
* ATS score improvement
* Job-specific CV customization
* Skill gap analysis
* Professional application email generation

---

## Technologies Used

* Python
* MCP (Model Context Protocol)
* FastMCP
* Groq LLM
* python-docx

---

## Author

Adil Hayat


