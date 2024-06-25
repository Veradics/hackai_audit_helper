import os
import openai
import streamlit as st

if "OPENAI_API_KEY" in st.secrets:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
else:
    st.error("No OpenAI API key provided. Set it in Streamlit secrets.")

# Debugging: Print the API key to check if it's loaded correctly (only for debugging purposes)
st.write(f"Debug: OpenAI API Key Loaded: {openai.api_key}")

# Check if the API key is set correctly
if not openai.api_key:
    st.error("No OpenAI API key provided. Set it in Streamlit secrets.")
else:
    st.write("OpenAI API key loaded.")

def send_prompt_to_assistant(prompt, assistant_id='asst_HGHaPA96oqQZJIX1532GTUoK'):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Or use the appropriate engine for your assistant
            prompt=prompt,
            max_tokens=1000,
            stop=None,
            n=1,
            temperature=0.5,
            user=assistant_id
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"An error occurred: {e}"

# Example Streamlit app to test the API key
def main():
    st.title('Test OpenAI API Key')
    prompt = st.text_input("Enter a prompt:")
    if st.button("Send to OpenAI"):
        if prompt:
            response = send_prompt_to_assistant(prompt)
            st.write("Response from OpenAI API:")
            st.write(response)
        else:
            st.write("Please enter a prompt.")

if __name__ == "__main__":
    main()