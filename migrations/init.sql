CREATE TABLE IF NOT EXISTS analyses (
    id SERIAL PRIMARY KEY,
    resume_text TEXT NOT NULL,
    job_description TEXT NOT NULL,
    match_score FLOAT NOT NULL,
    missing_skills TEXT,
    suggestions TEXT,
    ats_keywords TEXT,
    summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

