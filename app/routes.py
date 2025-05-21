from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from .services.gemini import GeminiService
from .config import settings

router = APIRouter()
gemini_service = GeminiService()

class ChatRequest(BaseModel):
    message: str
    userid: str

class ChatResponse(BaseModel):
    response: str
    userid: str

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat message and return a response
    """
    try:
        response = gemini_service.process_message(request.message, request.userid)
        return ChatResponse(response=response, userid=request.userid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 