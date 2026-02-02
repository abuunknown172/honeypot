import re

def extract_intelligence(text):
    upi_pattern = r'\b[\w.-]+@[\w.-]+\b'
    bank_pattern = r'\b\d{9,18}\b'
    url_pattern = r'(https?://\S+)'

    return {
        "upi_ids": list(set(re.findall(upi_pattern, text))),
        "bank_accounts": list(set(re.findall(bank_pattern, text))),
        "phishing_urls": list(set(re.findall(url_pattern, text)))
    }
