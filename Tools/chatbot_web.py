import os, re
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
print(api_key)


client = OpenAI(api_key=api_key)

# 3. Helper to trim incomplete sentences
def trim_to_last_sentence(text: str) -> str:
    if re.search(r'([\.!?])\s*$', text):
        return text
    last = max(text.rfind('.'), text.rfind('!'), text.rfind('?'))
    return text[: last+1] if last != -1 else text

# 4. Chat history held in memory for this demo
history = [
    {"role": "system", "content": "You are a helpful assistant."}
]

# 5. Flask setup
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # 6. Append user message
    history.append({"role": "user", "content": user_input})

    # 7. Call API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=history,
        max_tokens=150,
        temperature=0.7
    )
    raw = response.choices[0].message.content.strip()
    reply = trim_to_last_sentence(raw)

    # 8. Append assistant reply
    history.append({"role": "assistant", "content": reply})

    return jsonify({"reply": reply})

if __name__ == "__main__":
    # for dev only; in production use gunicorn or similar
    app.run(debug=True)
