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
CORS(app, resources={r"/api/": {"origins": ""}})

# Define the specific topic
SPECIFIC_TOPIC = "Surpac Software"

def create_flowchart_template(project_type):
    """Create a standardized flowchart template based on project type."""
    base_template = """
flowchart TB
    %% Project Start
    Start([Start]) --> Init[Project Initialization]
    
    %% Requirements Phase
    Init --> Req[Requirements Analysis]
    Req --> DataPrep[Data Preparation]
    
    %% Main Process Flow
    DataPrep --> MainProcess{Main Processing}
    
    %% Decision Points
    MainProcess -->|Success| Output[Generate Output]
    MainProcess -->|Failure| ErrorHandle[Error Handling]
    ErrorHandle --> Retry{Retry?}
    Retry -->|Yes| MainProcess
    Retry -->|No| Failure([End - Failure])
    
    %% Success Path
    Output --> Validate{Validation}
    Validate -->|Pass| Success([End - Success])
    Validate -->|Fail| RevisionNeeded[Revision Needed]
    RevisionNeeded --> MainProcess
    
    %% Styling
    classDef process fill:#a8d5ff,stroke:#333,stroke-width:2px;
    classDef decision fill:#ffe6cc,stroke:#333,stroke-width:2px;
    classDef start_end fill:#d5e8d4,stroke:#333,stroke-width:2px;
    
    class Start,Success,Failure start_end;
    class MainProcess,Validate,Retry decision;
    class Init,Req,DataPrep,Output,ErrorHandle,RevisionNeeded process;
    """
    
    # Add project-specific elements based on type
    if project_type == "data_processing":
        additional_steps = """
    %% Data Processing Specific Steps
    DataPrep --> DataValidation[Data Validation]
    DataValidation --> DataCleaning[Data Cleaning]
    DataCleaning --> DataTransform[Data Transformation]
    DataTransform --> MainProcess
    """
    elif project_type == "automation":
        additional_steps = """
    %% Automation Specific Steps
    Init --> SetupAuto[Setup Automation]
    SetupAuto --> ConfigCheck[Configuration Check]
    ConfigCheck --> Req
    """
    else:  # default template
        additional_steps = ""
    
    return base_template + additional_steps

def identify_request_type(input_text):
    """Determine the type of request being made."""
    analysis_prompt = (
        "Analyze the following request and categorize it as one of these types:\n"
        "1. 'general_question' - For general software usage questions\n"
        "2. 'project_flowchart' - For requests about project workflow or architecture\n"
        "3. 'tool_recommendation' - For requests about tool or feature suggestions\n"
        "4. 'project_guidance' - For detailed project implementation help\n"
        f"Request: '{input_text}'\n"
        "Respond with just the category name."
    )
    response = chat.send_message(analysis_prompt, stream=False)
    return response.text.strip().lower()

def is_on_topic(input_text):
    """Check if the input is related to the specific topic."""
    relevance_check_prompt = (
        f"Please evaluate if the following question relates to {SPECIFIC_TOPIC}:\n"
        f"Question: '{input_text}'\n"
        "Respond with 'Yes' if related, 'No' if not."
    )
    response = chat.send_message(relevance_check_prompt, stream=False)
    return response.text.strip().lower() == 'yes'

def is_detailed_request(input_text):
    """Check if the request requires detailed information."""
    detailed_keywords = ["explain", "details", "elaborate", "in-depth", "how to", "guide", "step by step"]
    return any(keyword in input_text.lower() for keyword in detailed_keywords)

def generate_flowchart_prompt(project_description):
    """Generate a prompt for creating a project flowchart."""
    return (
        f"As an expert in {SPECIFIC_TOPIC}, create a detailed flowchart using mermaid notation for:\n"
        f"{project_description}\n\n"
        "Requirements:\n"
        "1. Use the following node types:\n"
        "   - ([Text]) for Start/End nodes\n"
        "   - [Text] for Process nodes\n"
        "   - {Text} for Decision nodes\n"
        "   - ((Text)) for Database/Storage nodes\n"
        "2. Use clear direction indicators (TB for top to bottom)\n"
        "3. Include:\n"
        "   - Project initialization\n"
        "   - Main processing steps\n"
        "   - Decision points\n"
        "   - Error handling\n"
        "   - Success/failure paths\n"
        "4. Add styling using classDef for better visualization\n"
        "5. Include comments using %% for documentation\n\n"
        "Provide the complete mermaid flowchart code."
    )

def generate_tool_recommendations(project_description):
    """Generate tool recommendations based on project requirements."""
    return (
        f"As an expert in {SPECIFIC_TOPIC}, analyze and recommend tools for:\n"
        f"{project_description}\n\n"
        "Provide:\n"
        "1. Core Tools:\n"
        "   - List essential software/plugins required\n"
        "   - Version requirements\n"
        "   - Integration considerations\n"
        "2. Optional Tools:\n"
        "   - Additional tools for enhanced functionality\n"
        "   - Alternative options\n"
        "3. Justification:\n"
        "   - Why each tool is recommended\n"
        "   - Specific benefits and features\n"
        "4. Setup Requirements:\n"
        "   - System requirements\n"
        "   - Dependencies\n"
        "   - Installation order\n"
        "Format as a structured list with clear sections."
    )

def generate_project_guidance(project_description):
    """Generate detailed project implementation guidance."""
    return (
        f"As an expert in {SPECIFIC_TOPIC}, provide comprehensive implementation guidance for:\n"
        f"{project_description}\n\n"
        "Include:\n"
        "1. Project Setup:\n"
        "   - Environment preparation\n"
        "   - Required dependencies\n"
        "   - Initial configuration\n"
        "2. Implementation Steps:\n"
        "   - Detailed step-by-step instructions\n"
        "   - Code examples where relevant\n"
        "   - Configuration settings\n"
        "3. Best Practices:\n"
        "   - Optimization techniques\n"
        "   - Error handling\n"
        "   - Performance considerations\n"
        "4. Testing:\n"
        "   - Validation procedures\n"
        "   - Quality assurance steps\n"
        "5. Troubleshooting:\n"
        "   - Common issues\n"
        "   - Resolution steps\n"
        "Format as a detailed guide with clear sections and examples."
    )

def get_response(question):
    """Enhanced response generation based on request type."""
    # Handle simple greetings
    if question.lower() in ["hi", "hello", "hey"]:
        return f"Hello! How can I assist you with {SPECIFIC_TOPIC}?"

    # Check if the question is on topic
    if not is_on_topic(question):
        return (
            f"I'm specialized in {SPECIFIC_TOPIC}. I can help with:\n"
            "- General usage questions\n"
            "- Project planning and flowcharts\n"
            "- Tool recommendations\n"
            "- Detailed project guidance\n"
            "Please ask questions related to this software."
        )

    # Identify request type and generate appropriate response
    request_type = identify_request_type(question)
    
    try:
        if request_type == "project_flowchart":
            # Determine project type for flowchart template
            project_type = "default"
            if "data" in question.lower():
                project_type = "data_processing"
            elif "automation" in question.lower():
                project_type = "automation"
            
            base_flowchart = create_flowchart_template(project_type)
            prompt = generate_flowchart_prompt(question) + "\n\nBase template for reference:\n" + base_flowchart
        
        elif request_type == "tool_recommendation":
            prompt = generate_tool_recommendations(question)
        
        elif request_type == "project_guidance":
            prompt = generate_project_guidance(question)
        
        else:  # general_question
            if is_detailed_request(question):
                prompt = (
                    f"As an expert in {SPECIFIC_TOPIC}, provide a detailed answer to: {question}\n"
                    "Include examples and best practices where relevant."
                )
            else:
                prompt = f"Provide a concise answer about {SPECIFIC_TOPIC} for: {question}"
        
        response = chat.send_message(prompt, stream=False)
        return response.text.strip()
    
    except Exception as e:
        print(f"Error getting response from chat model: {e}")
        return "Error: Unable to retrieve response from model."

@app.route('/')
def home():
    return "Welcome to the Software Assistant Chatbot!"

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