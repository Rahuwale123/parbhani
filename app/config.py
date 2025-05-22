from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    GEMINI_API_KEY: "AIzaSyAWrqDp3qZvbZlI0FM9i_4mxUIui-TtW6c"
    APP_NAME: str = "Gemini Function Calling API"
    DEBUG: bool = False

    class Config:
        env_file = None

settings = Settings() 