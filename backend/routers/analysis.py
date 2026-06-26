import json
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models.database import get_db
from backend.models.schemas import AnalysisResponse
from backend.services.pdf_extractor import extract_text_from_pdf
from backend.services.llm_service import analyse_resume
from backend.services.db_service import (
    save_analysis,
    get_all_analyses,
    get_analysis_by_id,
)

router = APIRouter(prefix="/api", tags=["analysis"])


@router.post("/analyse", response_model=AnalysisResponse)
async def analyse(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    db: Session = Depends(get_db),
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    file_bytes = await file.read()
    resume_text = extract_text_from_pdf(file_bytes)

    if not resume_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from PDF")

    result = analyse_resume(resume_text, job_description)
    record = save_analysis(db, resume_text, job_description, result)

    return AnalysisResponse(
        id=record.id,
        match_score=record.match_score,
        missing_skills=json.loads(record.missing_skills),
        suggestions=json.loads(record.suggestions),
        ats_keywords=json.loads(record.ats_keywords),
        summary=record.summary,
        created_at=str(record.created_at),
    )


@router.get("/analyses", response_model=list[AnalysisResponse])
def get_analyses(db: Session = Depends(get_db)):
    records = get_all_analyses(db)
    return [
        AnalysisResponse(
            id=r.id,
            match_score=r.match_score,
            missing_skills=json.loads(r.missing_skills or "[]"),
            suggestions=json.loads(r.suggestions or "[]"),
            ats_keywords=json.loads(r.ats_keywords or "[]"),
            summary=r.summary or "",
            created_at=str(r.created_at),
        )
        for r in records
    ]


@router.get("/analyses/{analysis_id}", response_model=AnalysisResponse)
def get_analysis(analysis_id: int, db: Session = Depends(get_db)):
    record = get_analysis_by_id(db, analysis_id)
    if not record:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return AnalysisResponse(
        id=record.id,
        match_score=record.match_score,
        missing_skills=json.loads(record.missing_skills or "[]"),
        suggestions=json.loads(record.suggestions or "[]"),
        ats_keywords=json.loads(record.ats_keywords or "[]"),
        summary=record.summary or "",
        created_at=str(record.created_at),
    )
