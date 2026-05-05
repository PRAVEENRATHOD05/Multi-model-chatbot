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

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Enable CORS for all origins on specific routes

# Define the specific topic
SPECIFIC_TOPIC = "Adobe Software"

# Function to check if the input is related to the specific topic
def is_on_topic(input_text):
    relevance_check_prompt = (
        f"Please evaluate the relevance of the following question to the topic '{SPECIFIC_TOPIC}'. "
        f"Question: '{input_text}'. "
        "Respond with 'Yes' if closely related, or 'No' otherwise."
    )
    response = chat.send_message(relevance_check_prompt, stream=False)
    return response.text.strip().lower() == 'yes'

# Function to determine if the user is asking for detailed information
def is_detailed_request(input_text):
    detailed_request_keywords = ["explain", "details", "elaborate", "in-depth"]
    return any(keyword in input_text.lower() for keyword in detailed_request_keywords)

# Function to get a response from the model
def get_response(question):
    # Simple greeting responses
    if question.lower() in ["hi", "hello", "hey"]:
        return "Hello! How can I assist you with Surpac software?"

    # Check if the question is on topic
    if is_on_topic(question):
        if is_detailed_request(question):
            prompt = (
                f"You are an expert on the topic '{SPECIFIC_TOPIC}'. "
                "Please provide a detailed and informative answer to the following question: "
                f"{question}\nAnswer:"
            )
        else:
            prompt = (
                f"You are an expert on the topic '{SPECIFIC_TOPIC}'. "
                "Provide a short, concise answer to the following question: "
                f"{question}\nAnswer:"
            )
    else:
        prompt = (
            "I'm currently designed to assist with questions related to Adobe software. "
            "Please ask about Adobe, or specify if you need detailed information."
        )

    
    
    try:
        response = chat.send_message(prompt, stream=False)
        return response.text.strip()
    except Exception as e:
        print(f"Error getting response from chat model: {e}")
        return "Error: Unable to retrieve response from model."

# Define a basic route
@app.route('/')
def home():
    return "Welcome to the ChatGPT-like Flask App!"

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

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
