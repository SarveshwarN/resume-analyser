# AI Resume Analyser

An LLM-powered web application that analyses a candidate's resume against a job description — returning a match score, missing skills, ATS keyword gaps, and improved bullet point suggestions. All analyses are logged to PostgreSQL for tracking improvement over time.

🔗 **Live Demo:** https://resume-analyser-ai.streamlit.app  
📡 **API Docs:** https://resume-analyser-api-yy3i.onrender.com/docs

---

## Problem Statement

Job seekers struggle to tailor their resumes to specific job descriptions, leading to poor ATS (Applicant Tracking System) pass rates and low interview conversion. Manual resume review is time-consuming and subjective. This application automates resume-job fit analysis using LLMs, providing structured, actionable feedback instantly.

---

## Architecture

```
PDF Upload → PyMuPDF Text Extraction
          → OpenAI GPT-4o-mini (JSON mode)
          → Pydantic Validation
          → PostgreSQL Logging
          → Streamlit UI Display
```

---

## Tech Stack

| Layer | Technology | Reason |
|-------|-----------|--------|
| Backend API | FastAPI | Async support, automatic docs generation |
| AI Layer | OpenAI GPT-4o-mini | Cost-efficient, supports JSON mode for structured output |
| Data Validation | Pydantic v2 | Enforces schema on LLM output before database write |
| PDF Extraction | PyMuPDF | Fast, accurate text extraction from PDF resumes |
| Database ORM | SQLAlchemy | Type-safe database queries, session management |
| Database | PostgreSQL (Neon) | Persistent storage, tracks analysis history |
| Frontend | Streamlit | Rapid UI development for AI applications |
| Deployment | Render + Streamlit Cloud | Free tier, GitHub-integrated CI/CD |

---

## Core Features

- PDF resume text extraction via PyMuPDF
- LLM-powered job description comparison using GPT-4o-mini
- Match scoring (0–100%) with structured JSON output
- Missing skills identification
- ATS keyword gap analysis
- Resume bullet point improvement suggestions
- PostgreSQL logging of all analyses
- Analysis history tracking with timestamps

---

## Key Engineering Decisions

**Structured LLM Output:** Used OpenAI's `response_format: json_object` mode instead of parsing free text. This guarantees valid JSON responses and prevents parser failures in production.

**Pydantic Validation:** All LLM output is validated against a strict Pydantic schema before touching the database. Invalid match scores or missing fields raise errors immediately rather than corrupting data silently.

**Dependency Injection:** FastAPI's `Depends(get_db)` pattern used for database session management — sessions open per request and close automatically, preventing connection leaks.

**Environment Separation:** Local PostgreSQL for development, Neon cloud PostgreSQL for production. Same `DATABASE_URL` variable name, different values per environment — no code changes required between environments.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/analyse` | Upload PDF + job description, returns full analysis |
| GET | `/api/analyses` | Retrieve all past analyses ordered by date |
| GET | `/api/analyses/{id}` | Retrieve specific analysis by ID |
| GET | `/health` | Health check endpoint |

---

## Local Setup

### Prerequisites
- Python 3.11
- PostgreSQL running locally
- OpenAI API key with credits

### Steps

```bash
# Clone the repository
git clone https://github.com/SarveshwarN/resume-analyser.git
cd resume-analyser

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your credentials

# Run database migrations
# Execute migrations/init.sql in pgAdmin or psql

# Start the API
python -m uvicorn backend.main:app --reload

# Start the frontend (new terminal)
python -m streamlit run frontend/app.py
```

### Environment Variables

```
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=postgresql://user:password@localhost:5432/resume_analyser
```

---

## Project Structure

```
resume-analyser/
├── backend/
│   ├── main.py                  # FastAPI application entry point
│   ├── routers/
│   │   └── analysis.py          # API route definitions
│   ├── services/
│   │   ├── pdf_extractor.py     # PyMuPDF text extraction
│   │   ├── llm_service.py       # OpenAI API integration
│   │   └── db_service.py        # Database operations
│   ├── models/
│   │   ├── database.py          # SQLAlchemy models and session
│   │   └── schemas.py           # Pydantic validation schemas
│   └── prompts/
│       └── analysis_prompt.py   # LLM prompt engineering
├── frontend/
│   └── app.py                   # Streamlit UI
├── migrations/
│   └── init.sql                 # Database schema
├── .env.example
├── requirements.txt
└── README.md
```

---

## Known Limitations & Next Steps

| Limitation | Planned Improvement |
|-----------|-------------------|
| No user authentication | Add JWT-based auth so users only see their own analyses |
| No rate limiting | Add slowapi middleware to prevent API abuse |
| No unit tests | Add pytest test suite for services and routes |
| Free tier cold starts | Render free tier spins down after inactivity (50s delay) |
| Lists stored as JSON strings | Migrate to PostgreSQL ARRAY type |

---

## What I Learned

- Prompt engineering for structured output vs free-text LLM responses
- FastAPI dependency injection pattern for database session management
- Pydantic v2 schema validation for LLM output sanitisation
- Environment-based configuration for local vs production deployments
- End-to-end deployment pipeline: GitHub → Render → Streamlit Cloud

---

*Built as a portfolio project demonstrating AI engineering skills: LLM integration, REST API design, data validation, and cloud deployment.*
An LLM-powered web application that analyses a candidate's resume against a 
job description, returns a match score, identifies missing skills, suggests 
improved bullet points, and flags ATS keyword gaps.



