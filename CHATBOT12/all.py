from flask import Flask, jsonify, request
import os
from dotenv import load_dotenv
import google.generativeai as genai
from flask_cors import CORS, cross_origin

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Missing GOOGLE_API_KEY environment variable")
genai.configure(api_key=api_key)

chat = genai.GenerativeModel("gemini-pro").start_chat(history=[])

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

SPECIFIC_TOPIC = "surpac software"
SOFTWARE = "surpac"

def is_on_topic(input_text):
    relevance_check_prompt = (
        f"Please evaluate the relevance of the following question to the topic '{SPECIFIC_TOPIC}'. "
        f"Consider the core concepts, key terms, and overall context of the question. "
        f"Question: '{input_text}'. "
        f"Your response should be concise and limited to 'Yes' if the question is closely related to the topic, "
        f"or 'No' if it is not related."
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
    try:
        if is_flowchart_request(question):
            prompt = (
                f"Create a detailed step-by-step flowchart for '{SPECIFIC_TOPIC}', formatted as follows:\n\n"
                "Each step should be inside a rectangular box, with arrows connecting the steps in a vertical flow. "
                "List actions or details clearly within each step box.\n\n"
                "Use this layout structure exactly:\n"
                "              +----------------------------------+\n"
                "              |     Step 1                            |\n"
                "              |  - Action 1                           |\n"
                "              |  - Action 2                           |\n"
                "              +----------------------------------+\n"
                "                              |\n"
                "                              v\n"
                "              +----------------------------------+\n"
                "              |     Step 2                                   |\n"
                "              |  - Action 1                                  |\n"
                "              |  - Action 2                                  |\n"
                "              +----------------------------------+\n"
                "Please include a subheader related to each step after the step number."
            )
        else:
            prompt = (
                f"You are an expert on the topic '{SPECIFIC_TOPIC}'. "
                "Please provide a detailed and informative answer to the following question. "
                "Explain every relevant point clearly and comprehensively, covering all aspects of the topic related to the question:\n"
                f"Question: {question}\n"
                "Answer:"
            )
        
        response = chat.send_message(prompt, stream=False)
        return response.text
    except Exception as e:
        print(f"Error while getting response: {e}")
        return "There was an error while processing the request."

@app.route('/')
def home():
    return "Welcome to the ChatGPT-like Flask App!"

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
    app.run(debug=True, host="0.0.0.0", port=5000)
