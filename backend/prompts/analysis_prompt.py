def build_analysis_prompt(resume_text: str, job_description: str) -> str:
    return f"""
You are an expert ATS (Applicant Tracking System) and recruitment analyst.

Analyse the following resume against the job description provided.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return your analysis as a JSON object with exactly these keys:
{{
    "match_score": <integer 0-100>,
    "missing_skills": [<list of strings>],
    "suggestions": [<list of improved bullet point strings>],
    "ats_keywords": [<list of missing ATS keyword strings>],
    "summary": "<one sentence summary of the candidate fit>"
}}

Rules:
- match_score must be an integer between 0 and 100
- missing_skills must list specific technical or soft skills absent from the resume
- suggestions must be improved versions of weak resume bullet points
- ats_keywords must list important keywords from the job description missing in the resume
- Return only valid JSON. No extra text, no markdown, no explanation.
"""
