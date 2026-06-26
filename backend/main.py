from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers.analysis import router
from backend.models.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Resume Analyser API",
    description="AI-powered resume analysis against job descriptions",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
