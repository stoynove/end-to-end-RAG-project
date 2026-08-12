import streamlit as st
import requests
import os

# Configuration
# Read API URL from environment, fallback to localhost for development
API_URL = os.getenv("API_URL", "http://localhost:8000/api")

st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.title("📄 RAG Document Assistant")
st.markdown("Upload a PDF document and ask questions about its content.")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for file upload
with st.sidebar:
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if st.button("Process Document"):
        if uploaded_file is not None:
            with st.spinner("Processing document..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                try:
                    response = requests.post(f"{API_URL}/upload", files=files)
                    if response.status_code == 200:
                        data = response.json()
                        st.success(f"Success! {data['message']}")
                    else:
                        st.error(f"Failed to process document: {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Failed to connect to the backend API. Please make sure the backend is running.")
        else:
            st.warning("Please upload a file first.")

# Main chat interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask a question about your document..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        
        try:
            # Call backend API
            response = requests.post(f"{API_URL}/query", json={"question": prompt})
            
            if response.status_code == 200:
                answer = response.json().get("answer", "No answer provided.")
                message_placeholder.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                error_msg = f"Error from backend: {response.text}"
                message_placeholder.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
        except requests.exceptions.ConnectionError:
            error_msg = "Failed to connect to backend. Please ensure the backend server is running."
            message_placeholder.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
