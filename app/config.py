from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str = "AIzaSyAWrqDp3qZvbZlI0FM9i_4mxUIui-TtW6c"  # Replace with your actual API key
    APP_NAME: str = "Gemini Function Calling API"
    DEBUG: bool = False

settings = Settings() 