from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the generative model
chat = genai.GenerativeModel("gemini-pro").start_chat(history=[])

# Define the specific topic
SPECIFIC_TOPIC = "Surpac Software"  # Replace with your specific topic

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

# Function to get a response from the model (non-streaming, send in one go)
def get_response(question):
    # Define a prompt that provides context to the model
    prompt = (
        f"You are an expert on the topic '{SPECIFIC_TOPIC}'. "
        "Please provide a detailed and informative answer to the following question. "
        "Explain every relevant point clearly and comprehensively, covering all aspects of the topic related to the question:\n"
        f"Question: {question}\n"
        "Answer:"
    )
    
    response = chat.send_message(prompt, stream=False)  # Get full response at once
    return response.text  # Return the full response

app = Flask(__name__)

# Define a basic route
@app.route('/')
def home():
    return "Welcome to the Flask App!"
    return "hii"

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
    question = data.get('question', '')
    if not question:
        return jsonify({"error": "No question provided"}), 400

    response = get_response(question)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(port=5001,debug=True)
