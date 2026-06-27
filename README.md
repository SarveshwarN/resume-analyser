# AI Resume Analyser

An LLM-powered web application that analyses a candidate's resume against a 
job description, returns a match score, identifies missing skills, suggests 
improved bullet points, and flags ATS keyword gaps.

## Live Demo
- Frontend: https://resume-analyser-ai.streamlit.app
- API Docs: https://resume-analyser-api-yy3i.onrender.com/docs

## Tech Stack
- **Backend:** Python, FastAPI, SQLAlchemy
- **AI:** OpenAI GPT-4o-mini with structured JSON output
- **Database:** PostgreSQL (local), Neon (production)
- **Frontend:** Streamlit
- **PDF Extraction:** PyMuPDF
- **Deployment:** Render (API), Streamlit Cloud (UI)

## Architecture

- PDF Upload → PyMuPDF Text Extraction →

- OpenAI GPT-4o-mini Analysis → Pydantic Validation →

- PostgreSQL Logging → Streamlit UI Display

## Features
- PDF resume text extraction
- LLM-powered job description comparison
- Match scoring (0-100%)
- Missing skills identification
- Resume bullet point improvement suggestions
- ATS keyword gap analysis
- PostgreSQL logging of all analyses
- Analysis history tracking

## Local Setup

1. Clone the repository
   git clone https://github.com/SarveshwarN/resume-analyser.git
   cd resume-analyser

2. Create virtual environment
   python -m venv .venv
   .venv\Scripts\activate

3. Install dependencies
   pip install -r requirements.txt

4. Create .env file
   OPENAI_API_KEY=your_key_here
   DATABASE_URL=postgresql://user:password@localhost:5432/resume_analyser

5. Run the API
   python -m uvicorn backend.main:app --reload

6. Run the frontend
   python -m streamlit run frontend/app.py

## API Endpoints
- POST /api/analyse — Analyse resume against job description
- GET /api/analyses — Retrieve all past analyses
- GET /api/analyses/{id} — Retrieve specific analysis

