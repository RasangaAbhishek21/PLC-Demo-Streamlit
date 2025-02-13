import streamlit as st
import requests
import warnings

try:
    from langflow.load import upload_file
except ImportError:
    warnings.warn("Langflow provides a function to help you upload files to the flow. Please install langflow to use it.")
    upload_file = None

# Langflow API Configuration
BASE_API_URL = "http://127.0.0.1:7860"
FLOW_ID = "7f7c0f0b-053b-42ac-bed1-e0256d56468f"
ENDPOINT = ""  # You can set a specific endpoint name in the flow settings

def run_flow(message: str, endpoint: str) -> dict:
    """Send user input to Langflow and get a response."""
    api_url = f"{BASE_API_URL}/api/v1/run/{endpoint}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }

    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()  # Raise error if request fails
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Streamlit UI
st.title("Langflow AI Chatbot")
st.write("This chatbot interacts with a Langflow-powered AI model.")

# User Input
user_input = st.text_input("Enter your message:", "")

# Submit Button
if st.button("Send Message"):
    if user_input:
        # Call Langflow API
        response = run_flow(user_input, ENDPOINT or FLOW_ID)

        # Extract the chatbot response
        try:
            ai_text = response["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"]
        except (KeyError, IndexError, TypeError):
            ai_text = "Error: Could not extract response."

        # Display Response
        st.subheader("Response:")
        st.write(ai_text)
    else:
        st.warning("Please enter a message before sending.")
