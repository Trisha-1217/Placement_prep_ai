import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import engine

load_dotenv()

app = FastAPI(
    title="PlacementPrep AI - SDG 4 Evaluation API",
    description="Arena Evaluation API endpoint for PlacementPrep AI (UN SDG 4: Quality Education). Exposes standardized POST /chat contract.",
    version="1.0.0"
)

# Enable CORS for external evaluators and web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str = Field(..., description="Prompt or query sent to the AI Learning Tutor / Placement Mentor", examples=["Teach me the basics of linear regression as if I am a beginner, then give me three practice questions."])

class ChatResponse(BaseModel):
    response: str = Field(..., description="Chatbot response aligned with SDG 4: Quality Education")

@app.get("/")
def read_root():
    return {
        "project": "PlacementPrep AI",
        "sdg_track": "SDG 4 - Quality Education (AI Learning Tutor)",
        "status": "online",
        "endpoints": {
            "chat": "POST /chat",
            "health": "GET /health",
            "docs": "GET /docs"
        },
        "description": "AI-powered campus placement mock interview platform offering 4 rounds: CS Fundamentals, DSA, System Design, and HR Behavioral."
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "PlacementPrep AI API",
        "gemini_configured": engine.is_api_configured()
    }

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(payload: ChatRequest):
    """
    Mandatory Next Gen Chatbot Arena evaluation contract:
    POST /chat with JSON {"message":"..."} -> Response JSON {"response":"..."}
    """
    user_message = payload.message.strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="The 'message' field cannot be empty.")
    
    try:
        reply = engine.handle_arena_evaluator_message(user_message)
        return ChatResponse(response=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal processing error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"[*] Starting PlacementPrep AI API on http://0.0.0.0:{port}")
    uvicorn.run("api:app", host="0.0.0.0", port=port, reload=False)
