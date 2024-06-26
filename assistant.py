from typing_extensions import override
import time
import re

import streamlit as st
import openai
from openai import AssistantEventHandler



# should be secrets.toml file with OPENAI_API_KEY in streanlit folder
openai.api_key = st.secrets["OPENAI_API_KEY"]
    
client = openai.OpenAI()

assistant_id = 'asst_HGHaPA96oqQZJIX1532GTUoK'


# First, we create a EventHandler class to define
    # how we want to handle the events in the response stream.
class EventHandler(AssistantEventHandler):
    def __init__(self):
        super().__init__()  # Call the parent class's __init__ method
        self.response_text = ""
        self.response_placeholder = st.empty()
        self.response_placeholder.text('Analysis running...')

    @override
    def on_text_created(self, text) -> None:
        st.empty()
        self.response_placeholder.markdown(f"{self.response_text.strip()}") #**assistant >** 
        # st.write(f"\nassistant > ")

    @override
    def on_text_delta(self, delta, snapshot):
        self.response_text += sanitize_text(delta.value)
        self.response_placeholder.markdown(f"{self.response_text.strip()}") #**assistant >** 

    def on_tool_call_created(self, tool_call):
        st.empty()
        # st.write(f"\nassistant > {tool_call.type}\n")

    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                st.write(delta.code_interpreter.input)
            if delta.code_interpreter.outputs:
                st.write(f"\n\noutput >")
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        st.write(f"\n{output.logs}")


def sanitize_text(text):
    # Example regex to remove patterns like  
    clean_text = re.sub(r"【\d+:\d+†source】", "", text)
    return clean_text


# Define a function to get assistant response
def get_assistant_response(prompt):

    promp_upd = "Analyze the part of the annual report for TCFD compliance: " + prompt

    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": promp_upd
            }
        ]
    )

    # Then, we use the `stream` SDK helper 
    # with the `EventHandler` class to create the Run 
    # and stream the response.
    with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=assistant_id,
        event_handler=EventHandler(),
    ) as stream:
        stream.until_done()


# Define a function to get assistant response
def get_full_report_check(user_file):

    file = client.files.create(
                file=user_file, purpose="assistants"
            )
    
    # Create a new thread with a message that has the uploaded file's ID
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": "Analyze this annual report for TCFD compliance",
                "attachments": [
                    { "file_id": file.id, "tools": [{"type": "file_search"}] }
                ],
            }
        ]
    )

    # with the `EventHandler` class to create the Run 
    # and stream the response.
    with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=assistant_id,
        #instructions="Please address the user as Jane Doe. The user has a premium account.",
        event_handler=EventHandler(),
    ) as stream:
        stream.until_done()


def get_part_report_check(user_file):

    file = client.files.create(
                file=user_file, purpose="assistants"
            )
    
    # Create a new thread with a message that has the uploaded file's ID
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": "Analyze the part of the annual report for TCFD compliance",
                "attachments": [
                    { "file_id": file.id, "tools": [{"type": "file_search"}] }
                ],
            }
        ]
    )

    # with the `EventHandler` class to create the Run 
    # and stream the response.
    with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=assistant_id,
        #instructions="Please address the user as Jane Doe. The user has a premium account.",
        event_handler=EventHandler(),
    ) as stream:
        stream.until_done()
