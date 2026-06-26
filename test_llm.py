from backend.services.llm_service import analyse_resume

resume = """
John Smith
Python Developer
Skills: Python, SQL, Excel
Experience: 1 year data entry at ABC Corp
"""

job = """
We are looking for a Data Engineer with experience in:
Python, Apache Spark, Airflow, PostgreSQL, dbt, AWS, 
data pipeline development, ETL processes.
"""

result = analyse_resume(resume, job)
print("Match Score:", result.match_score)
print("Missing Skills:", result.missing_skills)
print("ATS Keywords:", result.ats_keywords)
print("Summary:", result.summary)
