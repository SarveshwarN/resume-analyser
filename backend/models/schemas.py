from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class AnalysisRequest(BaseModel):
    job_description: str = Field(..., min_length=50)


class AnalysisResult(BaseModel):
    match_score: int = Field(..., ge=0, le=100)
    missing_skills: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)
    ats_keywords: List[str] = Field(default_factory=list)
    summary: str


class AnalysisResponse(BaseModel):
    id: int
    match_score: int
    missing_skills: List[str]
    suggestions: List[str]
    ats_keywords: List[str]
    summary: str
    created_at: datetime

    class Config:
        from_attributes = True
