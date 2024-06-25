import streamlit as st
import openai


# Set up your OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

client = openai.OpenAI()

my_assistants = client.beta.assistants.list(
    order="desc",
    limit="20",
)
st.write(my_assistants.data)

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