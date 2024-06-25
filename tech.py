import magic
import tempfile
import time
import streamlit as st
import fitz 
import docx
import os
from dotenv import load_dotenv

import openai

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

def send_prompt_to_assistant(prompt, assistant_id='asst_HGHaPA96oqQZJIX1532GTUoK'):
    try:
        response = openai.Completion.create(
            engine="davinci-codex",  # Or use the appropriate engine for your assistant
            prompt=prompt,
            max_tokens=1000,
            stop=None,
            n=1,
            temperature=0.5,
            logprobs=None,
            user=assistant_id
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"An error occurred: {e}"

def check_file_type(file):
    mime = magic.Magic(mime=True)
    file_type = mime.from_buffer(file.read(1024))

    if file_type == 'application/pdf':
        return 'pdf'
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return 'docx'
    elif file_type == "text/plain":
        return 'txt'
    
    return file_type


# def get_file_text(file):
#     with open(file) as f:
#         text = f.read()

#     return text

# Function to extract text from PDF
def get_pdf_text(uploaded_file):
    try:
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
        return None

# Function to extract text from DOCX
def get_doc_text(uploaded_file):
    try:
        doc = docx.Document(uploaded_file)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        st.error(f"Error reading DOC file: {e}")
        return None

# Function to extract text from TXT
def get_txt_text(uploaded_file):
    try:
        return uploaded_file.read().decode("utf-8")
    except Exception as e:
        st.error(f"Error reading TXT file: {e}")
        return None


# Function to determine the file type and extract text
def get_file_text(uploaded_file, file_type):
    if file_type == "pdf":
        return get_pdf_text(uploaded_file)
    elif file_type == "vnd.openxmlformats-officedocument.wordprocessingml.document":
        return get_doc_text(uploaded_file)
    elif file_type == "plain":
        return get_txt_text(uploaded_file)
    else:
        st.error("Unsupported file type")
        return None


# create a temporary file
def save_text_to_tempfile(text):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    with open(temp_file.name, 'w') as file:
        file.write(text)
    return temp_file.name


# run analysis for full report
def run_full_report_analysis(file):
    short_feedback = """
        Your report is 20 pages long and provides information according 
        to selected industry evaluation criteria.
    """

    short_recommendations = """
        Improve description for you activities and add 
        more information to block 3.
    """

    full_analysis_text = """analysis text"""
    temp_filename = save_text_to_tempfile(full_analysis_text)

    results = {
        'standard_metric': 0.7,
        'best_practice_metric': 0.5,
        'short_feedback': short_feedback,
        'short_recommendations': short_recommendations,
        'analysis_file': temp_filename
    }

    time.sleep(5)

    return results


# run analysis for report block
def run_block_report_analysis(text):
    short_feedback = """
        Your text provides required information according 
        to selected industry standards.
    """

    short_recommendations = """
        Try adding information about emissions.
    """

    results = {
        'short_feedback': short_feedback,
        'short_recommendations': short_recommendations
    }
    time.sleep(5)

    return results


# generation of new report block using recommendations and new info
def generate_block(initial_block_text, new_info):
    generated_block_text = """
        During this year, the Company introduced new technologies 
        in production aimed at improving the environmental situation. 
        The amount of emissions decreased by 10%.
    """

    temp_filename = save_text_to_tempfile(generated_block_text)

    results ={
        'generated_block_text': generated_block_text,
        'generated_block_file': temp_filename
    }

    time.sleep(5)

    return results
