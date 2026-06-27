import streamlit as st
import requests
import json

API_URL = "https://resume-analyser-api-yy3i.onrender.com/api"

st.set_page_config(page_title="AI Resume Analyser", page_icon="📄", layout="wide")

st.title("📄 AI Resume Analyser")
st.markdown(
    "Upload your resume and paste a job description to get an AI-powered match analysis."
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Upload Resume")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

with col2:
    st.subheader("Job Description")
    job_description = st.text_area(
        "Paste the job description here",
        height=200,
        placeholder="Paste the full job description...",
    )

if st.button("Analyse Resume", type="primary"):
    if not uploaded_file:
        st.error("Please upload a PDF resume.")
    elif not job_description or len(job_description) < 50:
        st.error("Please enter a job description (minimum 50 characters).")
    else:
        with st.spinner("Analysing your resume..."):
            try:
                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "application/pdf",
                    )
                }
                data = {"job_description": job_description}
                response = requests.post(f"{API_URL}/analyse", files=files, data=data)

                if response.status_code == 200:
                    result = response.json()

                    st.success("Analysis complete!")
                    st.divider()

                    score = result["match_score"]
                    if score >= 70:
                        st.metric("Match Score", f"{score}%", delta="Good match")
                    elif score >= 40:
                        st.metric("Match Score", f"{score}%", delta="Needs improvement")
                    else:
                        st.metric("Match Score", f"{score}%", delta="Poor match")

                    st.divider()

                    col3, col4 = st.columns(2)

                    with col3:
                        st.subheader("Missing Skills")
                        for skill in result["missing_skills"]:
                            st.markdown(f"- {skill}")

                        st.subheader("ATS Keywords Missing")
                        for keyword in result["ats_keywords"]:
                            st.markdown(f"- {keyword}")

                    with col4:
                        st.subheader("Suggested Improvements")
                        for suggestion in result["suggestions"]:
                            st.markdown(f"- {suggestion}")

                    st.divider()
                    st.subheader("Summary")
                    st.info(result["summary"])

                else:
                    st.error(
                        f"Error: {response.json().get('detail', 'Something went wrong')}"
                    )

            except Exception as e:
                st.error(f"Could not connect to API: {e}")

st.divider()
st.subheader("Previous Analyses")

if st.button("Load History"):
    try:
        response = requests.get(f"{API_URL}/analyses")
        if response.status_code == 200:
            analyses = response.json()
            if analyses:
                for analysis in analyses:
                    with st.expander(
                        f"Analysis #{analysis['id']} — Score: {analysis['match_score']}% — {analysis['created_at']}"
                    ):
                        st.write("**Summary:**", analysis["summary"])
                        st.write(
                            "**Missing Skills:**", ", ".join(analysis["missing_skills"])
                        )
            else:
                st.info("No previous analyses found.")
    except Exception as e:
        st.error(f"Could not load history: {e}")
