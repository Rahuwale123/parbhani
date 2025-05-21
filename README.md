# Gemini Function Calling API

This is a FastAPI-based service that implements Google Gemini's function calling capabilities. It allows you to create AI-powered applications that can interact with external APIs and perform real-world actions.

## Features

- 🤖 Integration with Google's Gemini Pro model
- 🔄 Function calling capabilities
- 🚀 FastAPI backend
- 🔒 Secure API key management
- 📝 Swagger documentation

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file with your Gemini API key:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   APP_NAME="Gemini Function Calling API"
   DEBUG=True
   ```

## Running the Application

Start the server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Example Usage

Send a POST request to `/api/v1/chat` with a JSON body:
```json
{
    "message": "What's the weather in Tokyo?"
}
```

The API will:
1. Process your message using Gemini
2. If a function call is needed, execute it
3. Return the final response

## Available Functions

Currently implemented functions:
- `get_weather`: Get weather information for a location
- `get_stock_price`: Get current stock price for a symbol

## Security Notes

- Never commit your `.env` file
- Keep your API keys secure
- Validate all inputs before processing 