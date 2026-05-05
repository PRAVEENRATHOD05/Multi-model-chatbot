# 🤖 Multi-Model Chatbot

> An advanced multimodal AI chatbot application leveraging Google Generative AI (Gemini API) with Flask backend and web-based frontend interfaces.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Project Overview

This is a sophisticated multimodal AI chatbot system that integrates multiple backend implementations and frontend interfaces. It supports:

- **Text-to-Text**: Natural language conversations powered by Google Gemini AI
- **Image-to-Text**: Vision capabilities for analyzing and discussing images
- **Multiple Interfaces**: Flask REST API, HTML web interface, and Streamlit dashboard
- **Topic-Specific Responses**: Focused chatbot trained for specific domains (e.g., Surpac Software)

## ✨ Features

### Core Features
- 🧠 **Google Gemini Integration** - State-of-the-art generative AI models
- 🖼️ **Multimodal Support** - Handle both text and image inputs
- 🌐 **Web-Based UI** - User-friendly HTML/CSS/JavaScript interface
- 📊 **Streamlit Dashboard** - Interactive visualization interface
- 🔄 **CORS-Enabled** - Cross-origin resource sharing for API calls
- 🎯 **Topic Filtering** - Responds only to on-topic queries
- 💾 **Conversation History** - Maintains chat context across messages

### Technical Features
- RESTful API endpoints
- Environment-based configuration
- Modular architecture with multiple implementations
- Real-time response streaming
- Error handling and validation

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| **Python 3.8+** | Core language |
| **Flask 2.3** | REST API backend |
| **Streamlit 1.28** | Interactive web dashboard |
| **Google Generative AI** | AI model provider |
| **Flask-CORS** | Cross-origin support |
| **python-dotenv** | Environment configuration |
| **OpenCV** | Image processing |
| **Pillow** | Image manipulation |

## 📦 Project Structure

```
Multi-model-chatbot/
├── CHATBOT12/                    # Main application directory
│   ├── chatbot1.py              # Primary Flask-based chatbot
│   ├── chatbot2.py              # Alternative implementation
│   ├── chatbot3.py              # Extended features version
│   ├── chatbot4.py              # Advanced implementation
│   ├── vision.py                # Streamlit vision interface
│   ├── flowserver.py            # Flow-based server
│   ├── guidanceServer.py        # Guidance/help server
│   ├── guide.py                 # Guide module
│   ├── qa.py                    # Q&A functionality
│   ├── index.html               # Main HTML interface
│   ├── index2.html              # Alternative interface
│   ├── Login.html               # Authentication page
│   ├── chatbot.html             # Chat interface
│   ├── chatbot.css              # Main styling
│   ├── chatbot.js               # Chat functionality
│   ├── styles.css               # Additional styles
│   ├── styles2.css              # Alternative styles
│   ├── script.js                # Main scripts
│   └── script2.js               # Additional scripts
├── code/                         # C++ source code
│   └── code.c++
├── folder/                       # Alternative implementations
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
└── README.md                    # This file

```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git
- Google API Key for Generative AI

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/PRAVEENRATHOD05/Multi-model-chatbot.git
   cd Multi-model-chatbot
   ```

2. **Create Virtual Environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   ```bash
   # Copy the example file
   cp .env.example .env

   # Edit .env and add your Google API key
   # .env file should contain:
   # GOOGLE_API_KEY=your_actual_api_key_here
   ```

5. **Run the Application**

   **Option A: Flask REST API**
   ```bash
   python CHATBOT12/chatbot1.py
   # API will be available at http://localhost:5000
   ```

   **Option B: Streamlit Web Dashboard**
   ```bash
   streamlit run CHATBOT12/vision.py
   # Dashboard will open at http://localhost:8501
   ```

   **Option C: Alternative Implementations**
   ```bash
   python CHATBOT12/chatbot2.py
   python CHATBOT12/chatbot3.py
   ```

## 📡 API Endpoints

### Main Flask API (`chatbot1.py`)

#### POST `/api/chat`
Send a message to the chatbot.

**Request:**
```json
{
  "message": "What is Surpac Software?",
  "topic": "Surpac Software"
}
```

**Response:**
```json
{
  "response": "Surpac Software is...",
  "status": "success"
}
```

#### POST `/api/vision`
Send an image for analysis.

**Request:**
```json
{
  "image": "base64_encoded_image_string",
  "query": "What's in this image?"
}
```

**Response:**
```json
{
  "analysis": "Image analysis result...",
  "status": "success"
}
```

## 🔧 Configuration

### Environment Variables (`.env`)

```env
# Google Generative AI Configuration
GOOGLE_API_KEY=your_google_api_key_here

# Optional: API Configuration
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000
```

### Get Your Google API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key and paste it in `.env`

## 💡 Usage Examples

### Using Flask API with cURL

```bash
# Text chat
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "topic": "general"}'

# Image analysis
curl -X POST http://localhost:5000/api/vision \
  -H "Content-Type: application/json" \
  -d '{"image": "base64_data", "query": "Describe this"}'
```

### Using Python Requests

```python
import requests

# Chat endpoint
response = requests.post(
    'http://localhost:5000/api/chat',
    json={'message': 'What can you help with?', 'topic': 'general'}
)
print(response.json())
```

### Using Streamlit Interface

1. Run: `streamlit run CHATBOT12/vision.py`
2. Open browser to `http://localhost:8501`
3. Upload images and ask questions
4. Get real-time analysis and responses

## 🎯 Chatbot Capabilities

### Text Processing
- ✅ Natural language understanding
- ✅ Context-aware responses
- ✅ Conversation history
- ✅ Topic-specific filtering
- ✅ Multi-turn conversations

### Vision Processing
- ✅ Image analysis
- ✅ Object detection
- ✅ Text extraction (OCR)
- ✅ Visual question answering
- ✅ Image-based recommendations

## 📊 Implementation Details

### Multiple Implementations

- **chatbot1.py**: Primary implementation with full features
- **chatbot2.py**: Extended regex-based filtering
- **chatbot3.py**: Alternative architecture
- **chatbot4.py**: Advanced features
- **vision.py**: Streamlit-based vision interface

### Architecture

```
User Request
    ↓
API Endpoint
    ↓
Message Validation
    ↓
Topic Check
    ↓
Google Gemini AI
    ↓
Response Generation
    ↓
JSON Response
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Troubleshooting

### Issue: API Key not found
**Solution**: Ensure `.env` file exists and contains `GOOGLE_API_KEY`

### Issue: Port already in use
**Solution**: Change port in the code or kill existing process
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/macOS
lsof -i :5000
kill -9 <PID>
```

### Issue: Module not found
**Solution**: Reinstall requirements
```bash
pip install --upgrade -r requirements.txt
```

### Issue: CORS errors
**Solution**: Ensure Flask-CORS is properly configured in the code

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Praveen Rathod**
- GitHub: [@PRAVEENRATHOD05](https://github.com/PRAVEENRATHOD05)
- Email: mypersonal.ac55@gmail.com

## 🙏 Acknowledgments

- [Google Generative AI](https://ai.google/) for providing powerful AI models
- [Flask](https://flask.palletsprojects.com/) framework
- [Streamlit](https://streamlit.io/) for interactive dashboards
- Open source community

## 📚 Resources

- [Google Generative AI Documentation](https://ai.google/tutorials/python_quickstart/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Python-dotenv Guide](https://github.com/theskumar/python-dotenv)

## 📞 Support

If you encounter issues or have questions:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Review API documentation
3. Create an issue on GitHub
4. Contact the maintainer

---

**Last Updated**: May 2026
**Version**: 1.0.0
**Status**: Active Development
