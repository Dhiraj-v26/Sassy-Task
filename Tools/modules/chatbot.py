import os, re
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

history = [{
    "role": "system",
    "content": (
        "You are a helpful and concise assistant. "
        "Always respond in a well-structured way that ends the thought clearly "
        "within the token limit of 150, or provide a natural follow-up suggestion if the response is too short. "
        "Avoid ending with incomplete bullet points or sentences."
    )
}]
def trim_to_last_sentence(text: str) -> str:
    if re.search(r'([\.!?])\s*$', text):
        return text
    last = max(text.rfind('.'), text.rfind('!'), text.rfind('?'))
    return text[: last+1] if last != -1 else text

def is_natural_ending(text: str) -> bool:
    # Ends with proper punctuation or a full idea
    ends_well = re.search(r'[.!?]["\']?\s*$', text.strip())
    
    # Not ending on a standalone bullet point
    incomplete_list = re.search(r'\n?\d+\.\s*$', text.strip())
    
    return bool(ends_well) and not incomplete_list


def generate_reply(user_input: str) -> str:
    history.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=history,
        max_tokens=200,
        temperature=0.7
    )
    
    raw = response.choices[0].message.content.strip()

    # If the response is unnatural, append a graceful ending
    if not is_natural_ending(raw):
        raw = trim_to_last_sentence(raw)
        raw = raw.rstrip("1234567890. \n")  # remove hanging list markers
        raw += "\n\nLet me know if you'd like me to continue or explain further."
    
    history.append({"role": "assistant", "content": raw})
    return raw

