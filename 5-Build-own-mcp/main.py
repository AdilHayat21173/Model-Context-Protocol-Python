from job_analyzer import extract_job_requirements, suggest_cv_updates
from content import cv_data
from docx_updater import update_cv_docx
from pathlib import Path

# ==============================
# CV FILE PATH
# ==============================

base_dir = Path(__file__).resolve().parent
cv_path = base_dir / "Adil_Hayat_CV.docx"

# ==============================
# JOB DESCRIPTION
# ==============================

job_description = """Job Summary:
We are seeking an experienced AI / ML Engineer to design, build, and deploy enterprise-grade AI and machine learning solutions on Google Cloud Platform (GCP), with a strong focus on Vertex AI. The role involves working closely with business and engineering teams to deliver impactful AI use cases across Insurance and Healthcare, including predictive models, conversational AI, and intelligent decision support systems, while ensuring compliance with PDPL and responsible AI principles.
Location: Karachi/Lahore/Islamabad
Key Responsibilities:

Design, develop, and deploy machine learning models using Google Cloud Vertex AI
Build end-to-end ML pipelines for data preparation, training, evaluation, deployment, and serving
Identify and translate business problems into AI/ML solutions (e.g., fraud detection, claims prediction, risk scoring, clinical decision support)
Design and develop AI-powered features such as conversational AI, smart search, recommendations, and predictive analytics
Build and integrate AI solutions using Google AI Stack, including Vertex AI, Gemini APIs, and Dialogflow CX
Collaborate with Backend Engineers to expose AI models and capabilities as scalable microservices
Fine-tune and evaluate pre-trained models and LLMs for Insurance and Healthcare use cases
Implement MLOps best practices, including model versioning, CI/CD, monitoring, and automated retraining
Monitor model performance and data drift; implement retraining and optimization strategies
Ensure AI/ML solutions comply with PDPL, data privacy standards, and responsible AI principles (fairness, transparency, explainability)
Document models, pipelines, and decisions to support auditability and explainability
Requirements:

5+ years of experience in AI/ML engineering, data science, or applied AI
Strong hands-on experience with GCP Vertex AI (training, pipelines, model registry, endpoints)
Proficiency in Python and ML frameworks such as TensorFlow, PyTorch, or scikit-learn
Experience with MLOps tools and practices (Vertex Pipelines, Kubeflow, MLflow, CI/CD)
Hands-on experience with Google AI Stack, including Vertex AI and related services
Experience with LLMs, RAG architectures, and prompt engineering
Exposure to Gemini APIs and Dialogflow CX
Prior experience delivering Insurance or Healthcare AI/ML solutions
Knowledge of responsible AI, bias mitigation, and explainable ML techniques
Experience working in regulated environments with strict data privacy requirements"""

# ==============================
# STEP 1: Extract JD requirements
# ==============================

print("\n" + "=" * 50)
print("STEP 1: ANALYSING JOB DESCRIPTION")
print("=" * 50)

job_data = extract_job_requirements(job_description)

print("\nJOB ANALYSIS:\n")
print(job_data)

# ==============================
# STEP 2: Generate updated skill list
# ==============================

print("\n" + "=" * 50)
print("STEP 2: GENERATING UPDATED TECHNICAL SKILLS")
print("=" * 50)

suggestions = suggest_cv_updates(cv_data, job_data)

print("\nLLM SKILL OUTPUT:\n")
print(suggestions)

# ==============================
# STEP 3: Update CV DOCX
# ==============================

print("\n" + "=" * 50)
print("STEP 3: UPDATING CV DOCX")
print("=" * 50)

output_path = base_dir / "Adil_Hayat_CV_Updated.docx"

updated_file = update_cv_docx(
    cv_path=str(cv_path),
    suggestions=suggestions,
    output_path=str(output_path)
)

print(f"\nDone! Updated CV saved to: {updated_file}")