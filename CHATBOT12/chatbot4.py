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

SPECIFIC_TOPIC = "Surpac Mining Software"
SURPAC_MODULES = ["Geology", "Survey", "Block Modeling", "Mine Planning", 
                 "Geostatistics", "Grade Estimation", "Resource Estimation"]

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
        f"Create a detailed step-by-step flowchart for '{project_description}' in Surpac mining software. "
        "Format each step as:\n"
        "              +----------------------------------+\n"
        "              |     Step 1: [Mining Process]     |\n"
        "              |  - Specific Surpac Command       |\n"
        "              |  - Required Input/Output         |\n"
        "              +----------------------------------+\n"
        "                              |\n"
        "                              v\n"
        "Include:\n"
        "1. Data preparation\n"
        "2. Surpac-specific commands\n"
        "3. Quality control steps\n"
        "4. Output requirements"
    )
    return chat.send_message(flowchart_prompt, stream=False).text.strip()

def recommend_mining_tools(project_description):
    tools_prompt = (
        f"For this Surpac mining project:\n{project_description}\n"
        "Recommend:\n"
        "1. Required Surpac modules\n"
        "2. Input data formats\n"
        "3. Hardware requirements\n"
        "4. Specific toolbars\n"
        "Include practical settings and examples."
    )
    return chat.send_message(tools_prompt, stream=False).text.strip()

def get_mining_steps(project_description):
    steps_prompt = (
        f"Provide Surpac instructions for:\n{project_description}\n"
        "Include:\n"
        "1. Data preparation\n"
        "2. Surpac commands and menus\n"
        "3. Quality control steps\n"
        "4. Output generation"
    )
    return chat.send_message(steps_prompt, stream=False).text.strip()

def validate_mining_query(query):
    mining_keywords = ["surpac", "mining", "geology", "drill", "blast", 
                      "block model", "pit", "grade", "resource"]
    return any(keyword in query.lower() for keyword in mining_keywords)

def categorize_query(text):
    if any(word in text.lower() for word in ["flowchart", "workflow", "process"]):
        return "flowchart"
    elif any(word in text.lower() for word in ["tools", "software", "modules"]):
        return "tools"
    elif any(word in text.lower() for word in ["how to", "steps", "guide"]):
        return "steps"
    return "general"

def create_workflow_template(workflow_type):
    if workflow_type == "resource_estimation":
        steps = [
            ("Data Import", ["Import drillhole data", "Load geological models"]),
            ("Validation", ["Verify data integrity", "Check coordinates"]),
            ("Analysis", ["Run geostatistics", "Set parameters"]),
            ("Modeling", ["Create block model", "Run estimation"]),
            ("Validation", ["Verify results", "Generate reports"])
        ]
    elif workflow_type == "mine_planning":
        steps = [
            ("Setup", ["Import surfaces", "Define constraints"]),
            ("Design", ["Create pit design", "Add ramps"]),
            ("Planning", ["Set sequences", "Define targets"]),
            ("Optimization", ["Run scenarios", "Adjust plans"]),
            ("Output", ["Export designs", "Create reports"])
        ]
    else:
        steps = [
            ("Setup", ["Configure project", "Import data"]),
            ("Processing", ["Run analysis", "Apply methods"]),
            ("Validation", ["Check results", "Verify outputs"]),
            ("Reporting", ["Generate reports", "Export data"])
        ]
    
    flowchart = ""
    for i, (subheader, actions) in enumerate(steps, 1):
        flowchart += format_flowchart_step(i, subheader, actions)
    return flowchart

def get_response(question):
    if question.lower() in ["hi", "hello", "hey"]:
        return "Hello! How can I assist with Surpac mining software?"

    if not validate_mining_query(question):
        return "Please ask questions specific to Surpac mining software."

    try:
        query_type = categorize_query(question)
        
        if query_type == "flowchart":
            workflow_type = "general"
            if "resource" in question.lower():
                workflow_type = "resource_estimation"
            elif "planning" in question.lower():
                workflow_type = "mine_planning"
            return create_workflow_template(workflow_type)
            
        elif query_type == "tools":
            return recommend_mining_tools(question)
            
        elif query_type == "steps":
            return get_mining_steps(question)
            
        else:
            context_prompt = (
                f"As Surpac expert, answer:\n{question}\n"
                "Include specific commands and best practices."
            )
            return chat.send_message(context_prompt, stream=False).text.strip()
            
    except Exception as e:
        print(f"Error: {e}")
        return "Error processing query. Please try again."

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
