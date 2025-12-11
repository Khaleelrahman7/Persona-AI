from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import json
import os
from datetime import datetime

from memory_extraction import MemoryExtractor
from personality_engine import PersonalityEngine

app = FastAPI(title="Persona AI - Memory & Personality Engine")

# CORS middleware for React frontend
# Allow all origins for development and deployment flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # Must be False when using allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize modules
memory_extractor = MemoryExtractor()
personality_engine = PersonalityEngine()

# In-memory storage (in production, use a database)
user_memory_store: Dict[str, Dict] = {}


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    user_id: Optional[str] = "default_user"


class PersonalityRequest(BaseModel):
    messages: List[ChatMessage]
    personality: str  # "calm_mentor", "witty_friend", "therapist"
    user_id: Optional[str] = "default_user"


@app.get("/")
async def root():
    return {"message": "Persona AI API is running"}


@app.post("/api/extract-memory")
async def extract_memory(request: ChatRequest):
    """Extract memory from chat messages"""
    try:
        # Convert messages to format expected by memory extractor
        chat_history = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        # Extract memory
        memory = await memory_extractor.extract(chat_history)
        
        # Store memory
        if request.user_id not in user_memory_store:
            user_memory_store[request.user_id] = {
                "preferences": [],
                "emotional_patterns": [],
                "facts": [],
                "updated_at": None
            }
        
        # Merge new memory with existing
        user_memory_store[request.user_id]["preferences"].extend(memory.get("preferences", []))
        user_memory_store[request.user_id]["emotional_patterns"].extend(memory.get("emotional_patterns", []))
        user_memory_store[request.user_id]["facts"].extend(memory.get("facts", []))
        user_memory_store[request.user_id]["updated_at"] = datetime.now().isoformat()
        
        return {
            "extracted_memory": memory,
            "total_memory": user_memory_store[request.user_id]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/transform-personality")
async def transform_personality(request: PersonalityRequest):
    """Transform response with personality engine"""
    try:
        chat_history = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        # Get user memory for context
        user_memory = user_memory_store.get(request.user_id, {})
        
        # Generate response with personality
        response = await personality_engine.generate_response(
            chat_history=chat_history,
            personality=request.personality,
            user_memory=user_memory
        )
        
        return {
            "personality": request.personality,
            "response": response["response"],
            "before_response": response.get("before_response", ""),
            "after_response": response.get("after_response", "")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/memory/{user_id}")
async def get_memory(user_id: str):
    """Get stored memory for a user"""
    if user_id not in user_memory_store:
        return {"message": "No memory found for this user"}
    return user_memory_store[user_id]


@app.post("/api/chat")
async def chat_with_personality(request: PersonalityRequest):
    """Complete chat endpoint: extract memory + generate personality response"""
    try:
        chat_history = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        # Extract memory first
        memory = await memory_extractor.extract(chat_history)
        
        # Store memory
        if request.user_id not in user_memory_store:
            user_memory_store[request.user_id] = {
                "preferences": [],
                "emotional_patterns": [],
                "facts": [],
                "updated_at": None
            }
        
        user_memory_store[request.user_id]["preferences"].extend(memory.get("preferences", []))
        user_memory_store[request.user_id]["emotional_patterns"].extend(memory.get("emotional_patterns", []))
        user_memory_store[request.user_id]["facts"].extend(memory.get("facts", []))
        user_memory_store[request.user_id]["updated_at"] = datetime.now().isoformat()
        
        # Generate response with personality
        user_memory = user_memory_store[request.user_id]
        response = await personality_engine.generate_response(
            chat_history=chat_history,
            personality=request.personality,
            user_memory=user_memory
        )
        
        return {
            "extracted_memory": memory,
            "personality": request.personality,
            "response": response["response"],
            "before_response": response.get("before_response", ""),
            "after_response": response.get("after_response", "")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

