from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

chat = genai.GenerativeModel("gemini-pro").start_chat(history=[])

SPECIFIC_TOPIC = "Surpac Software"

def is_on_topic(input_text):
    relevance_check_prompt = (
        f"Please evaluate the relevance of the following question to the topic '{SPECIFIC_TOPIC}'. "
        f"Consider the core concepts, key terms, and overall context of the question. "
        f"Question: '{input_text}'. "
        "Your response should be concise and limited to 'Yes' if the question is closely related to the topic, "
        "or 'No' if it is not related. "
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
                f"Create a detailed step-by-step flowchart for '{SPECIFIC_TOPIC}', formatted exactly as follows:\n\n"
                "Each step should be inside a rectangular box, with arrows connecting the steps in a vertical flow. "
                "Clearly list actions or details inside each step box, using the layout structure below:\n\n"
                "              +----------------------------------+\n"
                "              |     Step 1: [Subheader]                      |\n"
                "              |  - Action 1                                  |\n"
                "              |  - Action 2                                  |\n"
                "              +----------------------------------+\n"
                "                              |\n"
                "                              v\n"
                "              +----------------------------------+\n"
                "              |     Step 2: [Subheader]                      |\n"
                "              |  - Action 1                                  |\n"
                "              |  - Action 2                                  |\n"
                "              +----------------------------------+\n\n"
                "Ensure that each step includes a subheader after the step number."
            )
            print("Flowchart prompt generated")
        else:
            prompt = (
                f"You are an expert on the topic '{SPECIFIC_TOPIC}'. "
                "Please provide a detailed and informative answer to the following question. "
                "Explain every relevant point clearly and comprehensively, covering all aspects of the topic related to the question:\n"
                f"Question: {question}\n"
                "Answer:"
            )
            print("General response prompt generated")

        # Use non-streaming to simplify debugging
        response = chat.send_message(prompt, stream=False)
        print("Model response:", response.text)  # Print the response for debugging

        return response.text

    except Exception as e:
        print("Error during response generation:", e)
        return "Error: Could not fetch the bot response. Please try again."
