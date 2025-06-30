import os, re
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

history = [{"role": "system", "content": "You are a helpful assistant."}]

def trim_to_last_sentence(text: str) -> str:
    if re.search(r'([\.!?])\s*$', text):
        return text
    last = max(text.rfind('.'), text.rfind('!'), text.rfind('?'))
    return text[: last+1] if last != -1 else text

def generate_reply(user_input: str) -> str:
    history.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=history,
        max_tokens=150,
        temperature=0.7
    )
    raw = response.choices[0].message.content.strip()
    reply = trim_to_last_sentence(raw)
    history.append({"role": "assistant", "content": reply})
    return reply
