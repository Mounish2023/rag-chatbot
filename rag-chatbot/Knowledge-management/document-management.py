import streamlit as st
import requests

st.title('Document Upload Interface')

def call_azure_function(file):
    url = "https://gamyam-func-app.azurewebsites.net/api/DataProcessing"

    # Depending on how your Azure function expects the input
    # you might send files in a different way
    # Here's one example where we're sending the file as binary data
    files = {
        'file': file    }
    response = requests.post(url, files=files)
    return response

st.header("Upload Document")
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    with st.spinner('Uploading the document ...'):
        response = call_azure_function(uploaded_file)
        if response.status_code == 200:
            st.success("Azure Function called successfully!")
            # Process response if needed
        else:
            st.error("Failed to call Azure Function.")
