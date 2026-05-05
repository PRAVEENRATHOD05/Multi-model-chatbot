# Multi-model-chatbot

A multimodal AI chatbot project using Flask, Streamlit, and Google Generative AI (Gemini API).

## Project Overview

This project implements a chatbot that can handle both text and image inputs using Google's Generative AI models.

## Setup Instructions

### Prerequisites
- Python 3.8+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/PRAVEENRATHOD05/Multi-model-chatbot.git
   cd Multi-model-chatbot
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your GOOGLE_API_KEY
   ```

5. **Run the application**
   - For Flask-based chatbot: `python CHATBOT12/chatbot1.py`
   - For Streamlit app: `streamlit run CHATBOT12/vision.py`

## Project Structure

```
CHATBOT12/          - Main chatbot implementation
├── chatbot1.py     - Flask-based chatbot
├── chatbot2.py     - Alternative implementation
├── vision.py       - Streamlit vision/image processing
├── *.html          - Frontend files
└── *.js, *.css     - Styling and scripts
```

## Features

- Text-based conversation with Gemini API
- Image processing and analysis
- Flask REST API backend
- Streamlit web interface
- CORS-enabled for cross-origin requests

## Dependencies

See `requirements.txt` for the complete list of dependencies.

## License

MIT License
