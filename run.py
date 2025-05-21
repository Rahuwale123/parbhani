import uvicorn
from app.config import settings
import os

def main():
    """
    Main function to run the FastAPI application
    """
    # Check if GEMINI_API_KEY is set
    if not settings.GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY environment variable is not set!")
        print("Please set it in your .env file or environment variables.")
        return

    # Configure uvicorn settings
    uvicorn_config = {
        "app": "app.main:app",
        "host": "0.0.0.0",
        "port": 8001,
        "reload": settings.DEBUG,
        "workers": 1,
        "log_level": "info" if settings.DEBUG else "warning"
    }

    print(f"Starting {settings.APP_NAME}...")
    print(f"Debug mode: {'ON' if settings.DEBUG else 'OFF'}")
    print(f"API Documentation available at: http://localhost:{uvicorn_config['port']}/docs")
    
    # Start the server
    uvicorn.run(**uvicorn_config)

if __name__ == "__main__":
    main() 