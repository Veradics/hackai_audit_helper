import magic
import tempfile
import time
import streamlit as st

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

def get_file_text(uploaded_file):
    # Ensure that the file is read correctly
    if uploaded_file is not None:
        try:
            file_text = uploaded_file.read().decode("utf-8")
            return file_text
        except Exception as e:
            st.error(f"Error reading file: {e}")
            return None
    else:
        st.error("No file uploaded")
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
