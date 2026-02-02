import os
from openai import OpenAI
from persona import persona_prompt

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def generate_reply(memory):
    messages = [
        {"role": "system", "content": persona_prompt}
    ]

    for msg in memory.get():
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.9
    )

    return response.choices[0].message.content.strip()
