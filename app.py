from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image

import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
os.environ["PATH"] += os.pathsep + "/usr/bin"
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    # Converting the PDF to Image
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read(), poppler_path="/usr/bin")
        
        first_page = images[0]
        
        # Convert into Bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode() # encode to base 64
            }
        ]
        return pdf_parts 
    else:
        raise FileNotFoundError("No file uploaded")

## StreamLit App
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload a Resume (PDF)", type="pdf")

if uploaded_file is not None:
    st.write("PDF uploaded successfully")
    
## THE 4 BUTTONS OF THE APPLICATION:    
submit1 = st.button("Tell me about the Resume")

submit2 = st.button("How can I improvise my skills")

submit3 = st.button("Percentage Match")

submit4 = st.button("What are the Keywords that are Missing")

# for the above buttons, we have an example input prompt:
input_prompt1 = """
You are an experienced HR with Tech Experience in the field of Data Science, Full Stack Web Development,
Devops, Data Analyst, your task is to review the provided resume 
against the job description for these profiles. Please share your professional evaluation on 
whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements. 
"""

input_prompt2 = """
You are an experienced and skilled ATS (Application Tracking System) scanner with a deep understanding of
data science, full stack web development, devops, data analyst, and deep ATS functionality. Your task is 
to evaluate the resume and then provide the candidate with insights on how they can improvise
their skills according to the job description provided. Jot down bullet points on how the candidate can
improvise their skills so that they can align with the job description.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of Data Science,
Full Stack Web Development, Devops, Data Analyst, and deep ATS functionality, your task is to 
evaluate the resume against the provided job description. Give me the percentage of match if the resume 
matches the job description. First the output should come as percentage and then keywords missing and 
last final thoughts. 
"""

input_prompt4 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of Data Science,
Full Stack Web Development, DevOps, and Data Analyst roles. The job description has several keywords
that are important for the role. Your task is to evaluate the resume against the provided job description
and then provide the candidate with insights on the keywords that are missing in the resume.
Provide the candidate with the missing keywords and how they can improvise their resume to 
align with the job description.
Jot down the missing keywords along with reasons why they are important for the role in a list manner."""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the Resume PDF")
        
elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the Resume PDF")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the Resume PDF")
        
elif submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt4, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the Resume PDF")
        


