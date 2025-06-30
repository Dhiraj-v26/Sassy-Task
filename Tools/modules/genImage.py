from openai import OpenAI
from dotenv import load_dotenv
import os
import base64
from io import BytesIO

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

def imgen(prompt):
    
    response = client.images.generate(
    model="dall-e-3", 
    prompt=prompt,
    size="1024x1024",  
    quality="standard",  
    response_format="b64_json"
    
    )

    base64_json = response.data[0].b64_json
    base64_json = "data:image/png;base64,"+base64_json
    # output_image_stream = BytesIO(image_bytes)
    # img_data = requests.get(image_url).content
    return base64_json


