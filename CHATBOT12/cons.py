import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the generative model
chat = genai.GenerativeModel("gemini-pro").start_chat(history=[])

# Define the specific topic
SPECIFIC_TOPIC = "surpac software"  # Replace with your specific topic

# Function to determine if user input is on-topic
def is_on_topic(input_text):
    # Prompt the model to determine the relevance of the input to the specific topic
    relevance_check_prompt = (
        f"Please evaluate the relevance of the following question to the topic '{SPECIFIC_TOPIC}'. "
        f"Consider the core concepts, key terms, and overall context of the question. "
        f"Question: '{input_text}'. "
        f"Your response should be concise and limited to 'Yes' if the question is closely related to the topic, "
        f"or 'No' if it is not related. "
    )
    response = chat.send_message(relevance_check_prompt, stream=False)
    return response.text.strip().lower() == 'yes'

# Function to get a response from the model
def get_response(question):
    # Define a prompt that provides context to the model
    prompt = (
        f"You are an expert on the topic '{SPECIFIC_TOPIC}'. "
        "Please provide a detailed and informative answer to the following question. "
        "Explain every relevant point clearly and comprehensively, covering all aspects of the topic related to the question:\n"
        f"Question: {question}\n"
        "Answer:"
    )
    
    response_chunks = []
    response = chat.send_message(prompt, stream=True)
    
    # Accumulate response chunks
    for chunk in response:
        response_chunks.append(chunk.text)
        
    full_response = ''.join(response_chunks)  # Join all chunks to form the complete response
    return full_response

# Streamlit page configuration
st.set_page_config(page_title="Q&A Demo", layout="wide")
st.title("Gemini LLM Application")

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Layout for input and button
input_col, button_col = st.columns([4, 1])
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
