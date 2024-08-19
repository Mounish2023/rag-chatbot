import streamlit as st
import requests

AZURE_FUNCTION_URL = 'https://gamyam-func-app.azurewebsites.net/api/userQuery'

# Function to generate an answer - placeholder for your actual logic
def generate_answer(question):
    """Sends a message to the Azure Function and returns the response."""
    # Prepare the request payload
    data = {'query': question}
    # Send the request
    response = requests.post(AZURE_FUNCTION_URL, json=data)
    # Return the response text (chatbot's response)
    return response.text

# Initialize the Streamlit app
st.title('Q&A Interface')

# Initialize session state to store questions and answers if not already set
if 'qa_list' not in st.session_state:
    st.session_state['qa_list'] = []

# Placeholder for all previous Q&A
qa_container = st.container()

# Display all previous Q&A
with qa_container:
    for q, a in reversed(st.session_state['qa_list']):
        st.text(f"Q: {q}")
        st.text_area("", value=f"A: {a}", height=100, disabled=True)

# Function to handle question submission
def handle_question_submission():
    question = st.session_state.question
    if question:  # Check if the question is not empty
        # Generate and store the answer
        answer = generate_answer(question)
        # Append the question-answer pair at the beginning of the list
        st.session_state.qa_list.insert(0, (question, answer))
        # Clear the input box after the question is submitted
        st.session_state.question = ""

# Text input for a new question
st.text_input("Ask your question here:", key="question", on_change=handle_question_submission)
# Button to submit the question
submit_button = st.button("Send", on_click=handle_question_submission)





