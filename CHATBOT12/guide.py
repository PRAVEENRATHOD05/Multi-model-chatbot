import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the generative model with history
chat = genai.GenerativeModel("gemini-pro").start_chat(history=[])

# Define the specific topic
SPECIFIC_TOPIC = "surpac software"  # Replace with your specific topic
SOFTWARE = "surpac"  # Hardcoded software name

# Function to determine if user input is on-topic
def is_on_topic(input_text):
    # Prompt the model to determine the relevance of the input to the specific topic
    relevance_check_prompt = (
        f"Please evaluate the relevance of the following question to the topic '{SPECIFIC_TOPIC}'. "
        f"Consider the core concepts, key terms, and overall context of the question. "
        f"Question: '{input_text}'. "
        f"Your response should be concise and limited to 'Yes' if the question is closely related to the topic, "
        f"or 'No' if it is not related."
    )
    response = chat.send_message(relevance_check_prompt, stream=False)
    return response.text.strip().lower() == 'yes'

# Function to extract the project name from user input
def extract_project_name(input_text):
    # Simple prompt to extract the project name from the user's input
    extraction_prompt = (
        f"Identify the project name in the following user input related to '{SPECIFIC_TOPIC}':\n"
        f"'{input_text}'\n"
        "Provide only the project name."
    )
    response = chat.send_message(extraction_prompt, stream=False)
    return response.text.strip()

# Function to get a response from the model
def get_response(question):
    # Extract the project name from the question
    project_name = extract_project_name(question)
    
    # Define a prompt to guide the user step-by-step through the project or experiment
    prompt = (
        f"You are an expert in using '{SOFTWARE}' for the project '{project_name}'. "
        "Your task is to guide the user in completing the project step-by-step in an optimized time. "
        "Explain every concept and step required to complete the project clearly and comprehensively. "
        "Additionally, mention common errors that users make during this process and how they can avoid them. "
        "If the user gets stuck at any point, provide guidance to help them resolve their confusion and proceed smoothly.\n"
        "Steps for the project:"
    )
    
    # Initialize a list to store chunks of the response
    response_chunks = []
    
    # Send the prompt and stream the response
    response = chat.send_message(prompt, stream=True)
    
    # Collect the response in chunks
    for chunk in response:
        response_chunks.append(chunk.text)
        
    # Combine all response chunks into a complete response
    full_response = ''.join(response_chunks)
    
    return full_response

# Streamlit page configuration
st.set_page_config(page_title="Time& Guidence Demo", layout="wide")
st.title("Gemini LLM Application")

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Layout for input and button
input_col, button_col = st.columns([4, 1])

# Input fields for the question
with input_col:
    input_text = st.text_input("Input your question here:", key="input")
with button_col:
    submit = st.button("Ask me")

# Handle user input and generate response
if submit and input_text:
    if is_on_topic(input_text):
        try:
            full_response = get_response(input_text)  # Get the full response
            st.session_state['chat_history'].append(("You", input_text))
            st.session_state['chat_history'].append(("Bot", full_response))  # Append full response to history
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning(f"The question is not related to '{SPECIFIC_TOPIC}'. Please ask a relevant question.")
elif submit:
    st.warning("Please fill in the input before submitting.")

# Display the latest response
if st.session_state['chat_history']:
    st.subheader("The Response is")
    last_role, last_text = st.session_state['chat_history'][-1]
    if last_role == "Bot":
        st.write(last_text)

# Display chat history using chat messages
st.subheader("The chat history is")
for role, text in st.session_state['chat_history']:
    if role == "You":
        st.markdown(f"<div style='text-align: right;'><b>{role}:</b> {text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align: left;'><i>{role}:</i> {text}</div>", unsafe_allow_html=True)
