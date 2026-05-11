from llm import ask_llm
import json


def extract_job_requirements(job_description: str):
    prompt = f"""
You are an expert ATS resume analyzer.

Analyze this job description and extract:

1. Must-have Skills
2. Nice-to-have Skills
3. Tools / Technologies
4. Cloud / Platforms
5. Keywords for ATS optimization

Return ONLY valid JSON.

Job Description:
{job_description}
"""

    response = ask_llm(prompt)

    try:
        return json.loads(response)
    except:
        return {"raw_response": response}


def suggest_cv_updates(cv_data: dict, job_data: dict):
    prompt = f"""
You are a professional resume writer and ATS expert.

Compare this CV against the job requirements and produce an updated Technical Skills section.

CV:
{cv_data['full_text']}

Job Requirements:
{job_data}

Instructions:
- Output ONLY the updated Technical Skills list, nothing else
- No explanations, no headers, no meta-sections, no tips
- Each line must follow EXACTLY this format:
  Category Label: tool1, tool2, tool3
- Merge existing CV skills with missing job skills into logical categories
- Keep it concise — values are comma-separated tools/technologies only, no sentences
- Use these category names as a guide (add or merge as needed):
  Machine Learning, Deep Learning & LLMs, Generative AI & Frameworks,
  Vertex AI & GCP, MLOps & CI/CD, Cloud & Infrastructure, Backend & APIs,
  Automation & Workflows, Responsible AI, Deployment & Monitoring,
  Version Control, Documentation & Auditability

Example output format (follow exactly):
Machine Learning: TensorFlow, PyTorch, scikit-learn
Deep Learning & LLMs: Fine-tuning, LLaMA 3, GPT-4, Prompt Engineering
Generative AI & Frameworks: LangChain, LangGraph, CrewAI, RAG
Vertex AI & GCP: Vertex AI, Vertex Pipelines, Gemini API, Dialogflow CX
MLOps & CI/CD: MLflow, GitHub Actions, Model Monitoring, Data Drift Detection
Cloud & Infrastructure: Google Cloud Platform (GCP), Docker, Kubernetes (GKE), Terraform
Backend & APIs: FastAPI, REST APIs, Microservices
Automation & Workflows: n8n, Zapier, Zoho Flow, Make.com
Responsible AI: Bias Mitigation, Explainable AI, PDPL Compliance
Deployment & Monitoring: Cloud Monitoring, Automated Retraining Pipelines
Version Control: Git, GitHub
Documentation & Auditability: Model Cards, Pipeline Documentation, Version Tracking
"""

    return ask_llm(prompt)