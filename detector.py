scam_keywords = [
    "urgent", "otp", "account blocked", "verify",
    "click link", "lottery", "reward", "upi",
    "bank", "kyc", "refund"
]

def detect_scam(text: str) -> bool:
    text = text.lower()
    return any(word in text for word in scam_keywords)
