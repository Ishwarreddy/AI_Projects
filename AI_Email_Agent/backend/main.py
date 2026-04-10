from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uvicorn

from Agent.Agent_1 import Agent_1

app = FastAPI(title="Email Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory email history (replace with DB in production)
email_history = []

class ChatRequest(BaseModel):
    message: str

class EmailRecord(BaseModel):
    id: int
    timestamp: str
    user_message: str
    agent_response: str
    status: str  # "sent" | "failed" | "info"
    recipient: Optional[str] = None

@app.get("/")
def root():
    return {"status": "Email Agent API is running"}

@app.post("/chat")
async def chat(request: ChatRequest):
    timestamp = datetime.now().isoformat()
    try:
        result = Agent_1.invoke({"messages": [("user", request.message)]})
        response = result["messages"][-1].content

        # Try to detect recipient from message
        recipient = None
        words = request.message.lower().split()
        for i, word in enumerate(words):
            if word in ("to", "email") and i + 1 < len(words):
                candidate = words[i + 1]
                if "@" in candidate:
                    recipient = candidate.strip(".,")
                    break

        record = {
            "id": len(email_history) + 1,
            "timestamp": timestamp,
            "user_message": request.message,
            "agent_response": response,
            "status": "sent" if "successfully" in response.lower() else "info",
            "recipient": recipient,
        }
        email_history.append(record)
        return {"response": response, "record": record}

    except Exception as e:
        record = {
            "id": len(email_history) + 1,
            "timestamp": timestamp,
            "user_message": request.message,
            "agent_response": str(e),
            "status": "failed",
            "recipient": None,
        }
        email_history.append(record)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history", response_model=List[EmailRecord])
def get_history():
    return email_history

@app.delete("/history")
def clear_history():
    email_history.clear()
    return {"message": "History cleared"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)