import os, re
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
print(api_key)


client = OpenAI(api_key=api_key)

def trim_to_last_sentence(text: str) -> str:
    if re.search(r'([\.!?])\s*$', text):
        return text
    last = max(text.rfind('.'), text.rfind('!'), text.rfind('?'))
    return text[:last+1] if last != -1 else text

def chat():
    history=[
        {
            "role":"system",
            "content":"You are a helpful assistant."
        }
    ]

    print("🤖 Chatbot is running. Type ‘quit’ to exit.\n")

    while True:
        userInput = input("You: ")

        if userInput.lower() in ("quit", "exit"):
            print("Goodbye!")
            break
        
        history.append({"role": "user", "content": userInput})

        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=history,
            max_tokens=150
        )
        # print(response)
        raw = response.choices[0].message.content.strip()
        reply = trim_to_last_sentence(raw)
        print(f"Bot: {reply}\n")
        history.append({"role": "assistant", "content": reply})
    
chat()