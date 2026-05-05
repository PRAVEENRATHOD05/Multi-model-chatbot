from flask import Flask, jsonify, request
import os
from dotenv import load_dotenv
import google.generativeai as genai
from flask_cors import CORS, cross_origin

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
chat = genai.GenerativeModel("gemini-pro").start_chat(history=[])
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

MINING_MODULES = {
    "block_modeling": ["resource estimation", "grade interpolation", "variography"],
    "geological": ["drillhole", "lithology", "stratigraphy", "sampling"],
    "planning": ["pit design", "scheduling", "optimization"],
    "validation": ["QAQC", "reconciliation", "reporting"]
}

def format_flowchart_step(step_number, subheader, actions):
    return (
        "              +----------------------------------+\n"
        f"              |     Step {step_number}: {subheader:<16} |\n"
        "".join(f"              |  - {action:<28} |\n" for action in actions) +
        "              +----------------------------------+\n"
        "                              |\n"
        "                              v\n"
    )

def generate_mining_flowchart(project_description):
    flowchart_prompt = (
        "As a Surpac mining expert, create a detailed flowchart for:\n"
        f"{project_description}\n"
        "Format exactly as follows:\n"
        "              +----------------------------------+\n"
        "              |     Step 1: [Mining Process]     |\n"
        "              |  - Specific Surpac Command       |\n"
        "              |  - Required Input/Output         |\n"
        "              +----------------------------------+\n"
        "                              |\n"
        "                              v\n"
        "Include:\n"
        "1. Data preparation steps\n"
        "2. Surpac-specific commands\n"
        "3. File formats and parameters\n"
        "4. Validation checkpoints\n"
        "5. Output requirements"
    )
    return chat.send_message(flowchart_prompt, stream=False).text.strip()

def recommend_mining_tools(project_description):
    tools_prompt = (
        f"For this Surpac mining project:\n{project_description}\n"
        "Provide detailed recommendations for:\n"
        "1. Required Surpac modules and versions\n"
        "2. Input data formats (e.g., CSV, DXF, STR)\n"
        "3. Hardware requirements\n"
        "4. Complementary software needs\n"
        "5. Specific toolbars and functions\n"
        "Include practical examples and typical settings."
    )
    return chat.send_message(tools_prompt, stream=False).text.strip()

def get_mining_steps(project_description):
    steps_prompt = (
        f"Create detailed Surpac instructions for:\n{project_description}\n"
        "Include:\n"
        "1. Data preparation:\n"
        "   - Required formats\n"
        "   - Validation checks\n"
        "2. Surpac process:\n"
        "   - Menu paths\n"
        "   - Command sequences\n"
        "   - Parameter settings\n"
        "3. Quality control:\n"
        "   - Validation methods\n"
        "   - Industry standards\n"
        "4. Output generation:\n"
        "   - Report formats\n"
        "   - Export options"
    )
    return chat.send_message(steps_prompt, stream=False).text.strip()

def validate_mining_query(query):
    mining_terms = set([
        term for module in MINING_MODULES.values() 
        for term in module
    ])
    query_words = set(query.lower().split())
    return bool(query_words.intersection(mining_terms))

def categorize_mining_query(text):
    text_lower = text.lower()
    categories = []
    
    for category, terms in MINING_MODULES.items():
        if any(term in text_lower for term in terms):
            categories.append(category)
    
    if not categories:
        categories = ['general']
    
    if "workflow" in text_lower or "process" in text_lower:
        categories.append("flowchart")
    if "tool" in text_lower or "software" in text_lower:
        categories.append("tools")
        
    return categories

def get_response(question):
    if not validate_mining_query(question):
        return (
            "Please ask questions specific to Surpac mining software. "
            "Include mining terminology or specific Surpac functions."
        )

    categories = categorize_mining_query(question)
    
    try:
        if "flowchart" in categories:
            return generate_mining_flowchart(question)
        elif "tools" in categories:
            return recommend_mining_tools(question)
        elif any(cat in categories for cat in MINING_MODULES.keys()):
            return get_mining_steps(question)
        else:
            context_prompt = (
                "As a Surpac expert, provide guidance on:\n"
                f"{question}\n"
                "Include specific commands and best practices."
            )
            return chat.send_message(context_prompt, stream=False).text.strip()
    except Exception as e:
        print(f"Error: {e}")
        return "Error processing mining software query. Please try again."

@app.route('/')
def home():
    return "Welcome to the Surpac Mining Software Assistant"

@app.route('/api/get_response', methods=['POST'])
@cross_origin()
def fetch_response():
    data = request.json
    question = data.get('question', '')
    if not question:
        return jsonify({"error": "Question required"}), 400
    
    response = get_response(question)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
