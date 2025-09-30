import streamlit as st
import os
import io
from openai import OpenAI
import PyPDF2

st.set_page_config(page_title="AI RESUME ANALYZER",page_icon="📃",layout="centered")
st.title("AI RESUME ANALYZER")
st.markdown("Upload Your Resume And Get AI Powered Feedback Tailored To Your Needs!")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)",type=["pdf","txt"])
job_role = st.text_input("Enter the job role that you're targeting (Optional)")

analyze = st.button("Analyze")

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")


with st.spinner("Analyzing"):
    if analyze and uploaded_file:
        try:
            file_content = extract_text_from_file(uploaded_file)

            if not file_content.strip():
                st.error("File does not have any content!")
                st.stop()

            prompt = f""" You are an expert career coach and resume analyst. 
            Your task is to evaluate a candidate's resume based on the target job role.
            Job Role: {job_role}
            Resume Content:{file_content}
            Instructions:
            1. Compare the resume against the key requirements, skills, and qualifications typically needed for the job role.
            2. Highlight strengths and relevant experiences that match the job role.
            3. Identify gaps or areas of improvement in the resume.
            4. Provide actionable recommendations to make the resume stronger for this role.
            5. Summarize your evaluation in a clear, concise, and structured format.
            """

            client = OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model = "gpt-3.5-turbo",
                messages = [
                    {"role":"system","content":"You are an expert resume reviewer with years of experience in HR and recruitment."},
                    {"role":"user","content":prompt}
                ],
                max_tokens=1024,
                temperature=0.7
            )

            st.markdown("### Analysis Results")
            st.markdown(response.choices[0].message.content)

        except Exception as e:
            st.error(f"An error occured:{str(e)}")
