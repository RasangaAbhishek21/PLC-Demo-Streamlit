import streamlit as st
import requests
import json
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

# Default Tweaks Dictionary
TWEAKS = {
    "ChatInput-lo9LS": {},
    "ParseData-fQUY1": {},
    "Prompt-I8ZcV": {},
    "ChatOutput-mRukD": {},
    "OpenAIEmbeddings-hXseQ": {},
    "OpenAIModel-T0uAv": {},
    "AstraDB-bsNqR": {}
}

def run_flow(message: str, endpoint: str, tweaks: dict = None, api_key: str = None) -> dict:
    """Send user input to Langflow and get a response."""
    api_url = f"{BASE_API_URL}/api/v1/run/{endpoint}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    
    if tweaks:
        payload["tweaks"] = tweaks

    headers = {"x-api-key": api_key} if api_key else None

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  # Raise error if request fails
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Streamlit UI
st.title("Langflow AI Chatbot")
st.write("This chatbot interacts with a Langflow-powered AI model.")

# User Input
user_input = st.text_input("Enter your message:", "")

# API Key (Optional)
api_key = st.text_input("Enter API Key (if required):", type="password")

# File Upload
uploaded_file = st.file_uploader("Upload a file (optional)", type=["txt", "csv", "json"])

# Submit Button
if st.button("Send Message"):
    if user_input:
        # Handle File Upload
        if uploaded_file and upload_file:
            tweaks = upload_file(
                file_path=uploaded_file.name,
                host=BASE_API_URL,
                flow_id=FLOW_ID,
                components=[],
                tweaks=TWEAKS
            )
        else:
            tweaks = TWEAKS

        # Call Langflow API
        response = run_flow(user_input, ENDPOINT or FLOW_ID, tweaks, api_key)

        # Extract the chatbot response
        try:
           ai_text = response["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"]
        except (KeyError, IndexError, TypeError):
           ai_text = "Error: Could not extract response."

        # Display Response
        st.subheader("Response:")
        # st.write(ai_text)
        
        
        #response = run_flow(user_input, ENDPOINT or FLOW_ID, tweaks, api_key)
        st.write(ai_text)
        # Display Response
    #     st.subheader("Response:")
    #     st.json(response)
    # else:
    #     st.warning("Please enter a message before sending.")