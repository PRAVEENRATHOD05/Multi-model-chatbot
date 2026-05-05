from flask import Flask, jsonify, request
import os
from dotenv import load_dotenv
import google.generativeai as genai
from flask_cors import CORS, cross_origin

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
    
    response = chat.send_message(prompt, stream=False)  # Get full response at once
    return response.text  # Return the full response

app = Flask(__name__)

# Define a basic route
@app.route('/')
def home():
    return "Welcome to the Flask App!"

# Define a simple API endpoint to get static data
@app.route('/api/data', methods=['GET'])
def get_data():
    data = {
        'name': 'Flask',
        'version': '1.0'
    }
    return jsonify(data)

# Define a POST API endpoint to post data
@app.route('/api/data', methods=['POST'])
def post_data():
    content = request.json
    return jsonify({"received_data": content}), 201

# Define an endpoint to check if input is on-topic
@app.route('/api/is_on_topic', methods=['POST'])
def check_on_topic():
    data = request.json
    question = data.get('question', '')
    if not question:
        return jsonify({"error": "No question provided"}), 400

    is_relevant = is_on_topic(question)
    return jsonify({"is_on_topic": is_relevant})

# Define an endpoint to get a model response for a question
@app.route('/api/get_response', methods=['POST'])
@cross_origin()
def fetch_response():
    data = request.json
    question = data.get(question, '')
    if not question:
        return jsonify({"error": "No question provided"}), 400

    response = get_response(question)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
