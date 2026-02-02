from fastapi import FastAPI, Request
from pydantic import BaseModel
import time

from memory import Memory
from detector import detect_scam
from extractor import extract_intelligence
from agent import generate_reply

app = FastAPI()
API_KEY = "test123"  # change later

from typing import Optional

class Message(BaseModel):
    message: str
    conversation_id: Optional[str] = "default"

@app.post("/honeypot")
async def honeypot(msg: Message, request: Request):

    api_key = request.headers.get("x-api-key")
    if api_key != API_KEY:
        return {"error": "Unauthorized"}

    memory = Memory(msg.conversation_id)
    memory.add("user", msg.message)

    # Full conversation text
    full_text = " ".join([m["content"] for m in memory.get()])

    scam_detected = detect_scam(full_text)

    if scam_detected:
        time.sleep(2)  # human delay
        reply = generate_reply(memory)
        memory.add("assistant", reply)
    else:
        reply = "Okay."

    # Extract intelligence from whole chat
    full_text = " ".join([m["content"] for m in memory.get()])
    intel = extract_intelligence(full_text)

    return {
        "scam_detection": scam_detected,
        "agent_response": reply,
        "engagement_metrics": {
            "conversation_turns": len(memory.get())
        },
        "extracted_intelligence": intel
    }
