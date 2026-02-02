from fastapi import FastAPI, Request
import time

from memory import Memory
from detector import detect_scam
from extractor import extract_intelligence
from agent import generate_reply

app = FastAPI()
API_KEY = "test123"

@app.post("/honeypot")
async def honeypot(request: Request):

    api_key = request.headers.get("x-api-key")
    if api_key != API_KEY:
        return {"error": "Unauthorized"}

    # READ RAW TEXT BODY (important)
    msg_text = (await request.body()).decode("utf-8")

    conversation_id = "default"

    memory = Memory(conversation_id)
    memory.add("user", msg_text)

    full_text = " ".join([m["content"] for m in memory.get()])
    scam_detected = detect_scam(full_text)

    if scam_detected:
        time.sleep(2)
        reply = generate_reply(memory)
        memory.add("assistant", reply)
    else:
        reply = "Okay."

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
