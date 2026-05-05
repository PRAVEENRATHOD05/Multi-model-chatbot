from flask import Flask, jsonify, request
import os
from dotenv import load_dotenv
import google.generativeai as genai
from flask_cors import CORS, cross_origin
import re

# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the generative model with history
chat = genai.GenerativeModel("gemini-pro").start_chat(history=[])

app = Flask(__name__)
CORS(app, resources={r"/api/": {"origins": ""}})

# Define Surpac-specific constants
SPECIFIC_TOPIC = "Surpac Mining Software"
SURPAC_MODULES = [
    "Geology", "Survey", "Block Modeling", "Mine Planning",
    "Geostatistics", "Grade Estimation", "Mine Design",
    "Resource Estimation", "Drill and Blast", "Strategic Planning"
]

def identify_surpac_module(input_text):
    """Identify which Surpac module the question relates to."""
    module_prompt = (
        f"Analyze which Surpac module this query relates to: '{input_text}'\n"
        f"Available modules: {', '.join(SURPAC_MODULES)}\n"
        "Respond with just the module name. If uncertain, respond with 'General'."
    )
    response = chat.send_message(module_prompt, stream=False)
    return response.text.strip()

def identify_request_type(input_text):
    """Determine the type of mining-related request."""
    analysis_prompt = (
        "Analyze the following Surpac-related request and categorize it as:\n"
        "1. 'general_question' - Basic Surpac usage queries\n"
        "2. 'workflow_design' - Mining workflow or process design\n"
        "3. 'technical_guidance' - Technical implementation help\n"
        "4. 'optimization' - Performance or process optimization\n"
        "5. 'data_handling' - Data import/export and management\n"
        "6. 'script_help' - Surpac scripting assistance\n"
        f"Request: '{input_text}'\n"
        "Respond with just the category name."
    )
    response = chat.send_message(analysis_prompt, stream=False)
    return response.text.strip().lower()

def is_surpac_related(input_text):
    """Verify if the query is related to Surpac software."""
    mining_keywords = [
        "surpac", "mining", "geology", "drill", "blast", "ore", "mineral",
        "deposit", "block model", "pit", "excavation", "grade", "resource",
        "reserve", "stope", "survey", "geostatistics", "kriging",
        "triangulation", "wireframe", "dtm", "string", "solid"
    ]
    return any(keyword in input_text.lower() for keyword in mining_keywords)

def create_mining_flowchart_template(workflow_type):
    """Create a standardized mining workflow flowchart."""
    base_template = """
flowchart TB
    %% Project Initialization
    Start([Start]) --> Init[Project Setup]
    Init --> DataImport[Import Mining Data]
    
    %% Data Validation
    DataImport --> Validate{Validate Data}
    Validate -->|Invalid| DataCleanup[Clean Data]
    DataCleanup --> Validate
    
    %% Main Processing
    Validate -->|Valid| Process{Process Type}
    """
    
    # Add workflow-specific elements
    if workflow_type == "resource_estimation":
        additional_steps = """
    Process -->|Resource Estimation| Geostat[Geostatistical Analysis]
    Geostat --> Variography[Variogram Modeling]
    Variography --> Estimation[Grade Estimation]
    Estimation --> BlockModel[Block Model Creation]
    BlockModel --> Validation[Resource Validation]
    """
    elif workflow_type == "mine_planning":
        additional_steps = """
    Process -->|Mine Planning| Design[Mine Design]
    Design --> Scheduling[Production Scheduling]
    Scheduling --> Optimization[Optimize Plan]
    Optimization --> CostAnalysis[Cost Analysis]
    """
    elif workflow_type == "drill_blast":
        additional_steps = """
    Process -->|Drill & Blast| Pattern[Pattern Design]
    Pattern --> Charge[Charge Calculation]
    Charge --> Timing[Timing Design]
    Timing --> BlastParams[Blast Parameters]
    """
    else:
        additional_steps = """
    Process -->|General| Analysis[Data Analysis]
    Analysis --> Report[Generate Reports]
    """
    
    # Add common ending
    ending = """
    %% Output Generation
    Report --> QA{Quality Check}
    QA -->|Pass| Export[Export Results]
    QA -->|Fail| Revise[Revision Needed]
    Revise --> Process
    Export --> End([End])
    
    %% Styling
    classDef process fill:#a8d5ff,stroke:#333,stroke-width:2px;
    classDef decision fill:#ffe6cc,stroke:#333,stroke-width:2px;
    classDef start_end fill:#d5e8d4,stroke:#333,stroke-width:2px;
    
    class Start,End start_end;
    class Process,Validate,QA decision;
    class Init,DataImport,DataCleanup,Report,Export,Revise process;
    """
    
    return base_template + additional_steps + ending

def generate_mining_workflow_prompt(project_description):
    """Generate a prompt for creating a mining workflow."""
    return (
        f"As a Surpac mining software expert, create a detailed workflow for:\n"
        f"{project_description}\n\n"
        "Requirements:\n"
        "1. Include these phases:\n"
        "   - Data import and validation\n"
        "   - Geological interpretation\n"
        "   - Resource estimation (if applicable)\n"
        "   - Mine design considerations\n"
        "   - Output generation\n"
        "2. Specify:\n"
        "   - Required Surpac modules\n"
        "   - Data formats and structures\n"
        "   - Quality control points\n"
        "   - Best practices for each step\n"
        "3. Consider:\n"
        "   - Data validation requirements\n"
        "   - Geostatistical parameters\n"
        "   - Mining constraints\n"
        "   - Regulatory requirements\n\n"
        "Provide the complete workflow using mermaid flowchart notation."
    )

def generate_technical_guidance(query):
    """Generate Surpac-specific technical guidance."""
    return (
        f"As a Surpac expert, provide technical guidance for:\n"
        f"{query}\n\n"
        "Include:\n"
        "1. Prerequisites:\n"
        "   - Required Surpac version\n"
        "   - Necessary modules and licenses\n"
        "   - Data requirements\n"
        "2. Step-by-step procedure:\n"
        "   - Menu navigation\n"
        "   - Parameter settings\n"
        "   - File handling\n"
        "3. Best practices:\n"
        "   - Data organization\n"
        "   - Validation steps\n"
        "   - Quality control\n"
        "4. Common issues and solutions:\n"
        "   - Typical problems\n"
        "   - Troubleshooting steps\n"
        "   - Performance optimization\n"
        "Format as a detailed technical guide."
    )

def generate_script_help(query):
    """Generate Surpac scripting guidance."""
    return (
        f"As a Surpac scripting expert, provide guidance for:\n"
        f"{query}\n\n"
        "Include:\n"
        "1. Script structure:\n"
        "   - Required functions\n"
        "   - Variable declarations\n"
        "   - Error handling\n"
        "2. Code examples:\n"
        "   - Basic implementation\n"
        "   - Advanced options\n"
        "   - Best practices\n"
        "3. Documentation:\n"
        "   - Function descriptions\n"
        "   - Parameter explanations\n"
        "   - Usage examples\n"
        "Format as a scripting tutorial with examples."
    )

def get_response(question):
    """Generate comprehensive Surpac-specific responses."""
    # Handle greetings
    if question.lower() in ["hi", "hello", "hey"]:
        return (
            "Hello! I'm your Surpac mining software assistant. I can help with:\n"
            "- General Surpac usage questions\n"
            "- Mining workflow design\n"
            "- Technical implementation guidance\n"
            "- Process optimization\n"
            "- Data handling procedures\n"
            "- Surpac scripting\n"
            "How can I assist you today?"
        )

    # Verify Surpac relevance
    if not is_surpac_related(question):
        return (
            "I'm specialized in Surpac mining software. Please ask questions related to:\n"
            "- Geological modeling\n"
            "- Resource estimation\n"
            "- Mine planning\n"
            "- Drill and blast design\n"
            "- Geostatistical analysis\n"
            "- Surpac data handling and scripting"
        )

    try:
        # Identify request type and relevant module
        request_type = identify_request_type(question)
        module = identify_surpac_module(question)
        
        # Generate appropriate response based on request type
        if request_type == "workflow_design":
            workflow_type = "general"
            if "resource" in question.lower():
                workflow_type = "resource_estimation"
            elif "planning" in question.lower():
                workflow_type = "mine_planning"
            elif "drill" in question.lower() or "blast" in question.lower():
                workflow_type = "drill_blast"
            
            base_flowchart = create_mining_flowchart_template(workflow_type)
            prompt = generate_mining_workflow_prompt(question) + "\n\nBase template:\n" + base_flowchart
        
        elif request_type == "technical_guidance":
            prompt = generate_technical_guidance(question)
        
        elif request_type == "script_help":
            prompt = generate_script_help(question)
        
        else:  # general_question, optimization, or data_handling
            prompt = (
                f"As a Surpac expert focusing on the {module} module, provide a detailed answer to:\n"
                f"{question}\n\n"
                "Include:\n"
                "- Specific Surpac tools and functions\n"
                "- Best practices and recommendations\n"
                "- Related modules or features\n"
                "- Practical examples where applicable"
            )
        
        response = chat.send_message(prompt, stream=False)
        return response.text.strip()
    
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Error: Unable to process your request. Please try again."

@app.route('/')
def home():
    return "Welcome to the Surpac Mining Software Assistant!"

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
    app.run(debug=True)