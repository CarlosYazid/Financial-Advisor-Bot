# Financial Advisor Bot - API Documentation

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)

## 1. Project Name
**Financial Advisor Bot** - AI-powered financial advisory API service

## 2. Brief Description
The Financial Advisor Bot is a sophisticated API service built with FastAPI that provides:
- AI-powered financial advisory through Google's Vertex AI
- Voice interaction capabilities (text-to-speech and speech-to-text)
- User authentication and management
- Secure API endpoints for financial consultations

The system is designed to help users manage their debts and financial obligations through conversational AI interactions.

## 3. Main Features

### Core Functionalities
- **AI Financial Advisory**: Integration with Google's Vertex AI for intelligent financial advice
- **Voice Interaction**: 
  - Text-to-speech conversion using Google Cloud Text-to-Speech
  - Speech-to-text transcription using Google Cloud Speech-to-Text
- **User Management**: 
  - CRUD operations for user accounts
  - Secure authentication with JWT tokens
- **Conversation System**: 
  - Chat history management
  - Context-aware financial advice

### Technical Features
- RESTful API with FastAPI
- OAuth2 password flow with JWT tokens
- Google Cloud services integration
- Modular architecture with clear separation of concerns
- Comprehensive error handling

## 4. Prerequisites

### System Requirements
- Python 3.9+
- pip package manager
- Google Cloud account with enabled services:
  - Vertex AI
  - Text-to-Speech API
  - Speech-to-Text API
  - Cloud Storage (optional)

### Environment Variables
You'll need to set up the following environment variables (`.env` file):

```ini
# Authentication
ALGORITHM=HS256
BCRYPT_ROUNDS=12
ACCESS_TOKEN_EXPIRE_MINUTES=30
SECRET=your-secret-key-here

# Google Cloud
GOOGLE_APPLICATION_VERTEX_AI_CREDENTIALS=path/to/service-account.json
GOOGLE_PROJECT_ID=your-project-id
GOOGLE_LOCATION=your-region
GOOGLE_MODEL_ID=gemini-pro

# Database
DB_ENDPOINT=https://your-database-api.com
DB_USER_ENDPOINT=/users
```

## 5. Installation

### Step-by-Step Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/Financial-Advisor-Bot.git
   cd Financial-Advisor-Bot
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Create a `.env` file in the root directory
   - Fill it with the required variables (see Prerequisites section)

5. **Run the application**:
   ```bash
   uvicorn main:app --reload
   ```

6. **Verify the installation**:
   - Visit `http://localhost:8000/docs` to access the Swagger UI
   - You should see the API documentation with all available endpoints

## 6. Usage

### Basic Workflow

1. **Authentication**:
   - First, obtain a JWT token by authenticating at `/login`
   - Use this token in the `Authorization` header for protected endpoints

2. **Financial Consultation**:
   - Send text messages to `/chatbot/talk` to get AI financial advice
   - Use `/audio` endpoints for voice interactions

3. **User Management**:
   - Manage user accounts through the `/user` and `/users` endpoints

### Example Session

1. Authenticate:
   ```bash
   curl -X POST "http://localhost:8000/login/" \
   -H "accept: application/json" \
   -H "Content-Type: application/x-www-form-urlencoded" \
   -d "username=user1&password=pass123"
   ```

2. Get financial advice:
   ```bash
   curl -X POST "http://localhost:8000/chatbot/talk" \
   -H "accept: application/json" \
   -H "Authorization: Bearer YOUR_TOKEN" \
   -H "Content-Type: application/json" \
   -d '{"id":1,"createdAt":"2024-01-01T00:00:00Z","userId":1,"message":"How can I reduce my debt?"}'
   ```

3. Convert response to audio:
   ```bash
   curl -X POST "http://localhost:8000/audio/" \
   -H "accept: application/json" \
   -H "Authorization: Bearer YOUR_TOKEN" \
   -H "Content-Type: application/json" \
   -d '{"id":1,"createdAt":"2024-01-01T00:00:00Z","userId":1,"message":"AI response text here"}'
   ```

## 7. Examples

### Example 1: Complete Financial Consultation Flow

```python
import requests
from datetime import datetime

# 1. Authenticate
auth_response = requests.post(
    "http://localhost:8000/login/",
    data={"username": "user1", "password": "pass123"}
)
token = auth_response.json()["access_token"]

# 2. Get financial advice
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

message = {
    "id": 1,
    "createdAt": datetime.utcnow().isoformat() + "Z",
    "userId": 1,
    "message": "I'm struggling with my $10,000 debt. What should I do?"
}

response = requests.post(
    "http://localhost:8000/chatbot/talk",
    headers=headers,
    json=message
)

print("AI Advice:", response.json()["response"])

# 3. Convert to audio
audio_response = requests.post(
    "http://localhost:8000/audio/",
    headers=headers,
    json={
        "id": 2,
        "createdAt": datetime.utcnow().isoformat() + "Z",
        "userId": 1,
        "message": response.json()["response"]
    }
)

print("Audio saved at:", audio_response.json()["audioPath"])
```

### Example 2: Voice-Based Interaction

```python
# After receiving audio file path from the previous example
# You can transcribe user's voice messages back to text

with open("user_voice_message.mp3", "rb") as audio_file:
    audio_content = audio_file.read()

transcription = requests.post(
    "http://localhost:8000/audio/transcribe",
    headers=headers,
    json={
        "id": 3,
        "createdAt": datetime.utcnow().isoformat() + "Z",
        "userId": 1,
        "message": "User voice message",
        "audioPath": "path/to/user_voice_message.mp3"
    }
)

print("Transcribed text:", transcription.json()["message"])
```

## 8. Project Structure

```
Financial-Advisor-Bot/
│
├── .gitignore          - Specifies intentionally untracked files
├── main.py             - Main application entry point
├── requirements.txt    - Python dependencies
│
├── controller/         - Business logic layer
│   ├── __init__.py
│   ├── audioController.py      - Handles audio processing
│   ├── authController.py       - Manages authentication
│   ├── chatBotController.py    - AI financial advisor logic
│   └── userController.py       - User management
│
├── model/              - Data models and utilities
│   ├── __init__.py
│   ├── models.py       - Pydantic models
│   └── utils.py        - Helper functions
│
├── routers/            - API route definitions
│   ├── __init__.py
│   ├── audio.py        - Audio-related endpoints
│   ├── auth.py         - Authentication endpoints
│   ├── chatbot.py      - AI chat endpoints
│   ├── user.py         - Single user endpoints
│   └── users.py        - Multiple users endpoints
│
└── static/             - Static files (created at runtime)
    └── media/
        └── audio/      - Stores generated audio files
```

## 9. API Reference

The API follows RESTful principles and uses JSON for data exchange. All endpoints are documented via Swagger UI at `/docs` when running the application.

### Authentication

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/login` | POST   | Authenticate and get JWT token |
| `/login/users/me` | GET | Get current user details |

### User Management

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/user` | GET | Get user by ID (query parameter) |
| `/user/{id}` | GET | Get user by ID (path parameter) |
| `/user` | POST | Create new user |
| `/user` | PUT | Update existing user |
| `/user` | DELETE | Delete user by ID (query parameter) |
| `/user/{id}` | DELETE | Delete user by ID (path parameter) |
| `/users` | GET | Get all users |

### Audio Processing

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/audio` | POST | Convert text to speech |
| `/audio/transcribe` | POST | Convert speech to text |

### Chatbot

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chatbot/talk` | POST | Get financial advice from AI |

## 10. How to Contribute

We welcome contributions! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature
   ```
3. **Commit your changes**:
   ```bash
   git commit -m "Add your feature"
   ```
4. **Push to the branch**:
   ```bash
   git push origin feature/your-feature
   ```
5. **Open a pull request**

### Contribution Guidelines
- Follow PEP 8 style guide
- Write clear commit messages
- Include tests for new features
- Update documentation when adding new features
- Keep the code modular and well-organized

## 11. Troubleshooting

### Common Issues

**1. Authentication Errors**
- Symptom: 401 Unauthorized errors
- Solution:
  - Verify your JWT token is valid and not expired
  - Check the `SECRET` environment variable matches between server and client
  - Ensure the `Authorization` header is properly formatted

**2. Google Cloud Service Errors**
- Symptom: 500 errors when using AI or audio features
- Solution:
  - Verify your Google Cloud credentials are correct
  - Check that the required APIs are enabled in your GCP project
  - Ensure your service account has proper permissions

**3. Audio File Generation Issues**
- Symptom: Audio files not being created
- Solution:
  - Check the `static/media/audio` directory exists and is writable
  - Verify Google Text-to-Speech API quotas haven't been exceeded

## 12. Changelog

### [1.0.0] - 2024-06-01
**Initial Release**
- Core financial advisory functionality
- User authentication system
- Voice interaction capabilities
- Basic user management

## 13. License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 14. Contact

For questions or support, please contact:

- **Project Maintainer**: Carlos Yazid
- **Email**: contact@carlospadilla.co
- **GitHub Issues**: [https://github.com/CarlosYazid/Financial-Advisor-Bot/issues](https://github.com/CarlosYazid/Financial-Advisor-Bot/issues)