import magic
import tempfile
import time
import streamlit as st
# import fitz 
# import docx

def centered_text(text):
    centered_text_html = f"""
    <div style="text-align: center;">
        {text}
    </div>
    """
    st.markdown(centered_text_html, unsafe_allow_html=True)


def display_response_from_file(file_path='response.txt'):
    try:
        with open(file_path, 'r') as file:
            response_text = file.read()
            st.markdown(response_text)  # Display the text with markdown formatting
    except FileNotFoundError:
        st.error("File not found. Please ensure the response file exists.")


# # Function to extract text from PDF
# def get_pdf_text(uploaded_file):
#     try:
#         pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
#         text = ""
#         for page_num in range(len(pdf_document)):
#             page = pdf_document.load_page(page_num)
#             text += page.get_text()
#         return text
#     except Exception as e:
#         st.error(f"Error reading PDF file: {e}")
#         return None

# # Function to extract text from DOCX
# def get_doc_text(uploaded_file):
#     try:
#         doc = docx.Document(uploaded_file)
#         text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
#         return text
#     except Exception as e:
#         st.error(f"Error reading DOC file: {e}")
#         return None

# Function to extract text from TXT
# def get_txt_text(uploaded_file):
#     try:
#         return uploaded_file.read().decode("utf-8")
#     except Exception as e:
#         st.error(f"Error reading TXT file: {e}")
#         return None


# # Function to determine the file type and extract text
# def get_file_text(uploaded_file, file_type):
#     if file_type == "pdf":
#         return get_pdf_text(uploaded_file)
#     elif file_type == "vnd.openxmlformats-officedocument.wordprocessingml.document":
#         return get_doc_text(uploaded_file)
#     elif file_type == "plain":
#         return get_txt_text(uploaded_file)
#     else:
#         st.error("Unsupported file type")
#         return None


# create a temporary file
def save_text_to_tempfile(text):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    with open(temp_file.name, 'w') as file:
        file.write(text)
    return temp_file.name
