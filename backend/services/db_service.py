import json
from sqlalchemy.orm import Session
from backend.models.database import Analysis
from backend.models.schemas import AnalysisResult


def save_analysis(
    db: Session, resume_text: str, job_description: str, result: AnalysisResult
) -> Analysis:
    record = Analysis(
        resume_text=resume_text,
        job_description=job_description,
        match_score=result.match_score,
        missing_skills=json.dumps(result.missing_skills),
        suggestions=json.dumps(result.suggestions),
        ats_keywords=json.dumps(result.ats_keywords),
        summary=result.summary,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_all_analyses(db: Session) -> list[Analysis]:
    return db.query(Analysis).order_by(Analysis.created_at.desc()).all()


def get_analysis_by_id(db: Session, analysis_id: int) -> Analysis | None:
    return db.query(Analysis).filter(Analysis.id == analysis_id).first()
