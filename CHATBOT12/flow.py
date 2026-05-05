import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

chat = genai.GenerativeModel("gemini-pro").start_chat(history=[])

SPECIFIC_TOPIC = "Surpac Software"  

def is_on_topic(input_text):
    relevance_check_prompt = (
        f"Please evaluate the relevance of the following question to the topic '{SPECIFIC_TOPIC}'. "
        f"Consider the core concepts, key terms, and overall context of the question. "
        f"Question: '{input_text}'. "
        f"Your response should be concise and limited to 'Yes' if the question is closely related to the topic, "
        f"or 'No' if it is not related. "
    )
    response = chat.send_message(relevance_check_prompt, stream=False)
    return response.text.strip().lower() == 'yes'

def is_flowchart_request(input_text):
    prompt = (
        f"Analyze the following user input to determine if it is a request for a flowchart: '{input_text}'. "
        "If the input is asking for a flowchart, respond with 'Yes'. Otherwise, respond with 'No'."
    )
    response = chat.send_message(prompt, stream=False)
    return response.text.strip().lower() == 'yes'

def get_response(question):
    if is_flowchart_request(question):
        prompt = (
    f"Create a detailed step-by-step flowchart for '{SPECIFIC_TOPIC}', formatted exactly as follows:\n\n"
    "Each step should be inside a rectangular box, with arrows connecting the steps in a vertical flow. "
    "Clearly list actions or details inside each step box, using the layout structure below:\n\n"
    "              +----------------------------------+\n"
    "              |     Step 1: [Subheader]                      |\n"
    "              |  - Action 1                                  |\n"
    "              |  - Action 2                                  |\n"
    "              +----------------------------------+\n"
    "                              |\n"
    "                              v\n"
    "              +----------------------------------+\n"
    "              |     Step 2: [Subheader]                      |\n"
    "              |  - Action 1                                  |\n"
    "              |  - Action 2                                  |\n"
    "              +----------------------------------+\n\n"
    "Ensure that each step includes a subheader after the step number."
)

    else:
        prompt = (
            f"You are an expert on the topic '{SPECIFIC_TOPIC}'. "
            "Please provide a detailed and informative answer to the following question. "
            "Explain every relevant point clearly and comprehensively, covering all aspects of the topic related to the question:\n"
            f"Question: {question}\n"
            "Answer:"
        )
    
    response_chunks = []
    response = chat.send_message(prompt, stream=True)
    
    for chunk in response:
        response_chunks.append(chunk.text)
        
    full_response = ''.join(response_chunks)
    return full_response

st.set_page_config(page_title="Flow chart Demo", layout="wide")
st.title("Gemini LLM Application")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input_col, button_col = st.columns([4, 1])
with input_col:
    input_text = st.text_input("Input your question here:", key="input")
with button_col:
    submit = st.button("Ask me")

if submit and input_text:
    if is_on_topic(input_text):
        try:
            full_response = get_response(input_text)
            st.session_state['chat_history'].append(("You", input_text))
            st.session_state['chat_history'].append(("Bot", full_response))
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning(f"The question is not related to '{SPECIFIC_TOPIC}'. Please ask a relevant question.")

if st.session_state['chat_history']:
    st.subheader("The Response is")
    last_role, last_text = st.session_state['chat_history'][-1]
    if last_role == "Bot":
        st.write(last_text)

st.subheader("The chat history is")
for role, text in st.session_state['chat_history']:
    if role == "You":
        st.markdown(f"<div style='text-align: right;'><b>{role}:</b> {text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align: left;'><i>{role}:</i> {text}</div>", unsafe_allow_html=True)
