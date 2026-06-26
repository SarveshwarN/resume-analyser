import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from backend.prompts.analysis_prompt import build_analysis_prompt
from backend.models.schemas import AnalysisResult


load_dotenv(override=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyse_resume(resume_text: str, job_description: str) -> AnalysisResult:
    prompt = build_analysis_prompt(resume_text, job_description)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert ATS analyst. Always respond with valid JSON only.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        response_format={"type": "json_object"},
    )

    raw = response.choices[0].message.content
    data = json.loads(raw)
    return AnalysisResult(**data)
