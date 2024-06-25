import streamlit as st
import openai
from typing_extensions import override
from openai import AssistantEventHandler

# Set up your OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

client = openai.OpenAI()

assistant_id = 'asst_HGHaPA96oqQZJIX1532GTUoK'

# Define a function to get assistant response
def get_assistant_response(prompt):
    thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )
    
    # First, we create a EventHandler class to define
    # how we want to handle the events in the response stream.
    class EventHandler(AssistantEventHandler):
        def __init__(self):
            super().__init__()  # Call the parent class's __init__ method
            self.response_text = ""

        @override
        def on_text_created(self, text) -> None:
            st.write(f"\nassistant > ")

        @override
        def on_text_delta(self, delta, snapshot):
            self.response_text += delta.value
            st.write(self.response_text.strip(), end="", flush=True)

        def on_tool_call_created(self, tool_call):
            st.write(f"\nassistant > {tool_call.type}\n")

        def on_tool_call_delta(self, delta, snapshot):
            if delta.type == 'code_interpreter':
                if delta.code_interpreter.input:
                    st.write(delta.code_interpreter.input)
                if delta.code_interpreter.outputs:
                    st.write(f"\n\noutput >")
                    for output in delta.code_interpreter.outputs:
                        if output.type == "logs":
                            st.write(f"\n{output.logs}")

    # Then, we use the `stream` SDK helper 
    # with the `EventHandler` class to create the Run 
    # and stream the response.
    with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=assistant_id,
        #instructions="Please address the user as Jane Doe. The user has a premium account.",
        event_handler=EventHandler(),
    ) as stream:
        stream.until_done()


# Streamlit app
st.title('OpenAI Assistant')

# Input prompt from user
user_input = st.text_input("Ask your assistant:")

if st.button('Get Response'):
    if user_input:
        get_assistant_response(user_input)
    else:
        st.write("Please enter a question.")