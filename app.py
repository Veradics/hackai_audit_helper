import streamlit as st
import openai


# Set up your OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

client = openai.OpenAI()


thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
)

run = client.beta.threads.runs.create_and_poll(
  thread_id=thread.id,
  assistant_id='asst_HGHaPA96oqQZJIX1532GTUoK',
  instructions="Please address the user as Jane Doe. The user has a premium account."
)


if run.status == 'completed': 
  messages = client.beta.threads.messages.list(
    thread_id=thread.id
  )
  st.write(messages)
else:
  st.write(run.status)

# Function to get response from the specific OpenAI assistant
def get_assistant_response(prompt, assistant_id):
    response = openai.ChatCompletion.create(
        model="text-davinci-003",  # or another model if specified for your assistant
        messages=[
            {"role": "system", "content": f"You are the assistant with ID {assistant_id}."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content'].strip()

# Streamlit app
st.title('OpenAI Assistant')

# Input prompt from user
user_input = st.text_input("Ask your assistant:")

if st.button('Submit'):
    if user_input:
        with st.spinner('Generating response...'):
            assistant_id = "asst_HGHaPA96oqQZJIX1532GTUoK"  # Your assistant ID
            response = get_assistant_response(user_input, assistant_id)
        st.success('Response:')
        st.write(response)
    else:
        st.warning('Please enter a question.')