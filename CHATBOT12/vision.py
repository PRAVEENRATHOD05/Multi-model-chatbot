from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Configure Google Gemini AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define the specific topic
SPECIFIC_TOPIC = "Surpac software"  # Replace with your specific topic

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-flash-001-tuning")

# Function to check if the input is on-topic
def is_on_topic(input_text):
    relevance_check_prompt = (
        f"Please evaluate the relevance of the following question to the topic '{SPECIFIC_TOPIC}'. "
        f"Consider the core concepts, key terms, and overall context of the question. "
        f"Question: '{input_text}'. "
        f"Your response should be concise and limited to 'Yes' if the question is closely related to the topic, "
        f"or 'No' if it is not related."
    )
    try:
        # Send the prompt to the model for relevance evaluation
        relevance_response = model.generate_content([relevance_check_prompt])
        
        if relevance_response.candidates and len(relevance_response.candidates) > 0:
            relevance_answer = relevance_response.candidates[0].content.parts[0].text.strip().lower()
            return relevance_answer == 'yes'
        else:
            return False
    except Exception as e:
        return False

# Function to get a response from the model based on user input and image
def get_response_from_gemini(input_text, image):
    try:
        # First, check if the input is relevant to the topic
        if is_on_topic(input_text):
            # Expert prompt to provide context to the model
            expert_prompt = (
                f"You are an expert in using '{SPECIFIC_TOPIC}'. You are able to solve any query related to this software. "
                f"Please assist the user with their question and help them understand the image provided."
            )

            # Concatenate expert prompt with user input
            combined_prompt = f"{expert_prompt} User's question: '{input_text}'."
            
            # Generate the content with both the expert prompt and the user's input
            response = model.generate_content([combined_prompt, image])
            
            # Check if there are any candidates returned in the response
            if response.candidates and len(response.candidates) > 0:
                candidate = response.candidates[0]

                # Access the text field within the parts list inside content
                if hasattr(candidate, 'content') and candidate.content.parts:
                    return candidate.content.parts[0].text
                else:
                    return "No text available in the candidate content."
            else:
                return "No response candidates returned from the model."
        else:
            return f"The input is not relevant to the topic: {SPECIFIC_TOPIC}. Please try again with a relevant question."
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="Gemini Pro Vision Image Demo")
st.header("Gemini Pro Vision Application (Topic: Surpac Software)")

input_text = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Tell me about the image.")

if submit:
    response = get_response_from_gemini(input_text, image)
    st.subheader("The Response is")
    st.write(response)
