import streamlit as st
import requests

# SambaNova API Details
API_ENDPOINT = "https://api.sambanova.ai/v1/chat/completions"
API_KEY = "f8f95aff-3535-470e-978a-6d8f29320497"

# Function to call SambaNova API
def call_sambanova_api(user_input):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }
    payload = {
        "stream": False,
        "model": "Meta-Llama-3.1-8B-Instruct",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": user_input},
        ],
    }

    try:
        response = requests.post(API_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

# Streamlit App
st.title("Streamlit App for OMI AI")

# Handling input from FastAPI
request_data = st.experimental_get_query_params()
user_input = request_data.get("user_input", [""])[0]

if user_input:
    # Get SambaNova response
    sambanova_response = call_sambanova_api(user_input)

    # Display the response
    st.write(f"User: {user_input}")
    st.write(f"SambaNova: {sambanova_response}")

# For local testing
if st.text_input("Test input"):
    st.experimental_rerun()
