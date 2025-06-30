from rembg import remove
from flask import Flask, request, render_template, send_file
from PIL import Image
import os
from io import BytesIO
from modules.removebg import bgrm
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/rmbg', methods=['GET', 'POST'])
def handle_rmbg():
    if request.method == 'POST':
        if 'image' not in request.files:
            return "No file uploaded", 400
        print('step1')
        file = request.files['image']
        print('step2')

        if file.filename == '':
            return "No file selected", 400
        
        output_image_stream = bgrm(file)
        # # input_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        # image = Image.open(file)
        # print('step3')

        # input_bytes = BytesIO()
        # image.save(input_bytes, format='PNG')
        # print('step4')

        # input_bytes = input_bytes.getvalue()
        # print('step5')

        # output_bytes = remove(input_bytes)
        # print('step6')

        # output_image_stream = BytesIO(output_bytes)
        # print('step7')

        return send_file(output_image_stream, mimetype='image/png')
    return render_template('bgrm.html')
        
if __name__ == '__main__':
    app.run()
        # with open(input_path, 'rb') as i:
        #     with open(output_path, 'wb') as o:
        #         input = i.read()
        #         output = remove(input)
        #         o.write(output)

# input_path = '20240414_023300.jpg'
# output_path = 'output.png'
# rmbg(input_path ,output_path)
