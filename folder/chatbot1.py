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

def analyze_user_input(question):
    analysis_prompt = f"""
    Analyze this user query about Surpac mining software: "{question}"
    
    Determine:
    1. Query type (choose one):
       - Flowchart request (workflow visualization)
       - Tool recommendation
       - Step-by-step guidance
       - General question
       
    2. Specific module/area (if applicable):
       - Geology
       - Survey
       - Block Modeling
       - Mine Planning
       - Geostatistics
       - Grade Estimation
       - Resource Estimation
       
    3. Key requirements:
       - Data types needed
       - Specific tools mentioned
       - Expected outputs
       
    Return analysis in this format:
    Query type: [type]
    Module: [module]
    Requirements: [key requirements]
    """
    
    analysis = chat.send_message(analysis_prompt, stream=False).text.strip()
    return parse_analysis_response(analysis)

def parse_analysis_response(analysis):
    lines = analysis.split('\n')
    parsed = {
        'query_type': '',
        'module': '',
        'requirements': []
    }
    
    for line in lines:
        if line.startswith('Query type:'):
            parsed['query_type'] = line.split(':')[1].strip().lower()
        elif line.startswith('Module:'):
            parsed['module'] = line.split(':')[1].strip()
        elif line.startswith('Requirements:'):
            parsed['requirements'] = [req.strip() for req in line.split(':')[1].strip().split(',')]
    
    return parsed

def format_flowchart_step(step_number, subheader, actions):
    return (
        "              +----------------------------------+\n"
        f"              |     Step {step_number}: {subheader:<16} |\n"
        "".join(f"              |  - {action:<28} |\n" for action in actions) +
        "              +----------------------------------+\n"
        "                              |\n"
        "                              v\n"
    )

def generate_mining_flowchart(project_description, module):
    flowchart_prompt = (
        f"Create a detailed step-by-step flowchart for '{project_description}' "
        f"specifically for the {module} module in Surpac mining software.\n"
        "Format each step as:\n"
        "              +----------------------------------+\n"
        "              |     Step 1: [Mining Process]     |\n"
        "              |  - Specific Surpac Command       |\n"
        "              |  - Required Input/Output         |\n"
        "              +----------------------------------+\n"
        "                              |\n"
        "                              v\n"
        "Include:\n"
        "1. Data preparation specific to {module}\n"
        "2. Surpac-specific commands and menus\n"
        "3. Quality control steps\n"
        "4. Output requirements\n"
        "5. Best practices for this module"
    )
    return chat.send_message(flowchart_prompt, stream=False).text.strip()

def recommend_mining_tools(project_description, module, requirements):
    tools_prompt = (
        f"For this Surpac mining project in the {module} module:\n{project_description}\n"
        "With these requirements: " + ", ".join(requirements) + "\n\n"
        "Recommend:\n"
        f"1. Specific Surpac tools and its functions used for {project_description}\n"
        "2. Required input data formats and structures\n"
        "3. Hardware and system requirements\n"
        f"4. Relevant toolbars and menu locations of{project_description}\n"
        f"5. Optimal settings and configurations for {project_description}\n"
        f"6. Common pitfalls to avoid in this {project_description}\n"
        "Include practical examples and typical use cases."
    )
    return chat.send_message(tools_prompt, stream=False).text.strip()

def get_mining_steps(project_description, module, requirements):
    steps_prompt = (
        f"Provide detailed Surpac instructions for:\n{project_description}\n"
        f"Module: {module}\n"
        "Requirements: " + ", ".join(requirements) + "\n\n"
        "Include:\n"
        "1. Initial setup and data preparation\n"
        "2. Specific Surpac commands with menu paths\n"
        "3. Parameter settings and configurations\n"
        "4. Quality control checkpoints\n"
        "5. Output generation and validation\n"
        "6. Troubleshooting tips"
    )
    return chat.send_message(steps_prompt, stream=False).text.strip()

def get_response(question):
    if question.lower() in ["hi", "hello", "hey"]:
        return "Hello! How can I assist with Surpac mining software?"

    try:
        # Analyze user input first
        analysis = analyze_user_input(question)
        query_type = analysis['query_type']
        module = analysis['module']
        requirements = analysis['requirements']
        
        if 'flowchart' in query_type:
            return generate_mining_flowchart(question, module)
        elif 'tool' in query_type:
            return recommend_mining_tools(question, module, requirements)
        elif 'step' in query_type or 'guidance' in query_type:
            return get_mining_steps(question, module, requirements)
        else:
            context_prompt = (
                f"As a Surpac expert, specifically for the {module} module, answer:\n{question}\n"
                "Include:\n"
                "1. Specific commands and menu locations\n"
                "2. Best practices and recommendations\n"
                "3. Common issues and solutions\n"
                "4. Relevant examples"
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