from fastapi import FastAPI, Request
import time
import requests
import threading

from memory import Memory
from detector import detect_scam
from extractor import extract_intelligence
from agent import generate_reply

app = FastAPI()
API_KEY = "test123"


def send_final_callback(session_id, memory, intel, scam_detected):
    payload = {
        "sessionId": session_id,
        "scamDetected": scam_detected,
        "totalMessagesExchanged": len(memory.get()),
        "extractedIntelligence": {
            "bankAccounts": intel.get("bank_accounts", []),
            "upiIds": intel.get("upi_ids", []),
            "phishingLinks": intel.get("phishing_urls", []),
            "phoneNumbers": [],
            "suspiciousKeywords": []
        },
        "agentNotes": "Scammer used urgency and phishing tactics"
    }

    try:
        requests.post(
            "https://hackathon.guvi.in/api/updateHoneyPotFinalResult",
            json=payload,
            timeout=3
        )
    except:
        pass


@app.post("/honeypot")
async def honeypot(request: Request):

    api_key = request.headers.get("x-api-key")
    if api_key != API_KEY:
        return {"status": "error", "message": "Unauthorized"}

    data = await request.json()

    session_id = data.get("sessionId")
    message = data.get("message", {}).get("text", "")
    history = data.get("conversationHistory", [])

    memory = Memory(session_id)

    for msg in history:
        memory.add(msg["sender"], msg["text"])

    memory.add("user", message)

    full_text = " ".join([m["content"] for m in memory.get()])
    scam_detected = detect_scam(full_text)

    if scam_detected:
        reply = generate_reply(memory)
        memory.add("assistant", reply)
    else:
        reply = "Okay."

    # Prepare intelligence
    full_text = " ".join([m["content"] for m in memory.get()])
    intel = extract_intelligence(full_text)

    # 🔥 RETURN RESPONSE FIRST (critical)
    response = {
        "status": "success",
        "reply": reply
    }

    # 🔥 Run GUVI callback in background thread
    if scam_detected:
        threading.Thread(
            target=send_final_callback,
            args=(session_id, memory, intel, scam_detected),
            daemon=True
        ).start()

    return response
