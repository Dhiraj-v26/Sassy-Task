# from flask import Flask, request, render_template, send_file, jsonify
# from modules.calculator import calculate
# from rembg import remove
# from PIL import Image
# import os, re
# from io import BytesIO
# from modules.removebg import bgrm
# from dotenv import load_dotenv, find_dotenv
# from openai import OpenAI

# app = Flask(__name__)

# UPLOAD_FOLDER = 'uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.route('/calc', methods=['GET', 'POST'])
# def calc():
#     if request.method == 'POST':
#         num1 = int(request.form.get('num1'))
#         num2 = int(request.form.get('num2'))
#         operator = request.form.get('operator')

#         # if num1.strip() == '' or num2.strip() == '':
#         #     return "<h1>Invalid number. Please enter a number.</h1>"
        
#         # if operator == "+":
#         #     ans = num1 + num2
#         # elif operator == "-":
#         #     ans = num1 - num2
#         # elif operator == "*":
#         #     ans = num1*num2
#         # else:
#         #     if num2 != 0:
#         #         ans = num1 / num2
#         #     else:
#         #         raise ZeroDivisionError
        
#         ans = calculate(num1,num2,operator)
        
#         return {"ans":ans}
#     else:
#         return render_template('calc.html')
    
# @app.route('/rmbg', methods=['GET', 'POST'])
# def handle_rmbg():
#     if request.method == 'POST':
#         if 'image' not in request.files:
#             return "No file uploaded", 400
#         print('step1')
#         file = request.files['image']
#         print('step2')

#         if file.filename == '':
#             return "No file selected", 400
        
#         output_image_stream = bgrm(file)
#         # # input_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#         # image = Image.open(file)
#         # print('step3')

#         # input_bytes = BytesIO()
#         # image.save(input_bytes, format='PNG')
#         # print('step4')

#         # input_bytes = input_bytes.getvalue()
#         # print('step5')

#         # output_bytes = remove(input_bytes)
#         # print('step6')

#         # output_image_stream = BytesIO(output_bytes)
#         # print('step7')

#         return send_file(output_image_stream, mimetype='image/png')
#     return render_template('bgrm.html')


# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/chat", methods=["POST"])
# def chat():
#     user_input = request.json.get("message", "").strip()
#     if not user_input:
#         return jsonify({"error": "No message provided"}), 400

#     print("🤖 Chatbot is running. Type ‘quit’ to exit.\n")

    

#     return jsonify({"reply": reply})






from flask import Flask, request, render_template, send_file, jsonify
from modules.calculator import calculate
from modules.removebg import bgrm
from modules.chatbot import generate_reply
from modules.genImage import imgen
from io import BytesIO
import os
import base64

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ==== ROUTE: Calculator ====
@app.route('/calc', methods=['GET', 'POST'])
def calc():
    if request.method == 'POST':
        try:
            num1 = float(request.form.get('num1'))
            num2 = float(request.form.get('num2'))
            operator = request.form.get('operator')
            ans = calculate(num1, num2, operator)
            return {"ans": ans}
        except Exception as e:
            return {"error": str(e)}, 400
    else:
        return render_template('calc.html')

# ==== ROUTE: Background Remover ====
@app.route('/rmbg', methods=['GET', 'POST'])
def handle_rmbg():
    if request.method == 'POST':
        if 'image' not in request.files:
            return "No file uploaded", 400
        file = request.files['image']
        if file.filename == '':
            return "No file selected", 400
        try:
            output_image_stream = bgrm(file)
            return send_file(output_image_stream, mimetype='image/png')
        except Exception as e:
            return str(e), 500
        
    else:
        return render_template('bgrm.html')

@app.route("/")
def home():
    return render_template("home.html")


# ==== ROUTE: Chatbot API ====
@app.route("/chat", methods=["GET","POST"])
def chat():
    if request.method == "POST":

        user_input = request.json.get("message", "").strip()
        if not user_input:
            return jsonify({"error": "No message provided"}), 400
        try:
            reply = generate_reply(user_input)
            return jsonify({"reply": reply})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return render_template('index.html')
    
@app.route('/imgen', methods=["GET", "POST"])
def gen_img():
    if request.method == "POST":
        prompt = request.json.get("message", "").strip()

        if not prompt:
            return jsonify({"error": "No Prompt provided"}), 400
        
        try:
            image = imgen(prompt)
            return jsonify({"image": image})
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return render_template("imgen.html")

if __name__ == "__main__":
    app.run(debug=True)
