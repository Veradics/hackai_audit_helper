import os
import openai
import streamlit as st
import time

# Check if the key exists in st.secrets
if "OPENAI_API_KEY" in st.secrets:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
else:
    st.error("No OpenAI API key provided. Set it in Streamlit secrets.")

def upload_file(file):
    try:
        response = openai.File.create(
            file=openai.FileHandle(file),
            purpose='code_interpreter'
        )
        return response.id
    except Exception as e:
        return f"An error occurred: {e}"

def send_file_to_assistant(file_id, assistant_id='asst_HGHaPA96oqQZJIX1532GTUoK'):
    try:
        client = openai.Client()
        assistant = client.beta.assistants.retrieve(assistant_id)
        job = assistant.jobs.create(
            tool="code_interpreter",
            tool_resources={
                "code_interpreter": {
                    "file_ids": [file_id]
                }
            }
        )
        return job
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    st.title('Upload a file and evaluate it with OpenAI Assistant')
    uploaded_file = st.file_uploader("Choose a file", type=['csv'])

    if uploaded_file is not None:
        st.write("File uploaded successfully.")
        file_id = upload_file(uploaded_file)
        if file_id:
            st.write(f"File ID: {file_id}")
            job = send_file_to_assistant(file_id)
            if isinstance(job, str):
                st.error(job)  # Display error message if any
            else:
                st.write("Job created successfully. Waiting for the result...")
                # Poll for job completion
                while True:
                    client = openai.Client()
                    job = client.beta.jobs.retrieve(job.id)
                    if job.status == "succeeded":
                        st.write("Job completed successfully.")
                        st.write(job.result)
                        break
                    elif job.status == "failed":
                        st.error("Job failed.")
                        break
                    st.write("Waiting for job to complete...")
                    time.sleep(5)
        else:
            st.write("Failed to upload the file.")

if __name__ == "__main__":
    main()