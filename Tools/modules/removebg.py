from rembg import remove
from PIL import Image
from io import BytesIO

def bgrm(file):
    image = Image.open(file)
    input_bytes = BytesIO()
    image.save(input_bytes, format='PNG')
    input_bytes = input_bytes.getvalue()

    output_bytes = remove(input_bytes)
    output_image_stream = BytesIO(output_bytes)
    return output_image_stream
