
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, jsonify
import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Epiphy Academy!'

@app.route("/classify", methods=["POST"])
def classify():
    data = request.get_json()

    if not data or "image_base64" not in data:
        return jsonify({"error": "image_base64 required"}), 400

    image_base64 = data["image_base64"]
    prompt = data.get("prompt", "tell me about the image")  # default prompt

    try:
        response = openai.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt},
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    ]
                }
            ],
            max_output_tokens=400
        )

        return jsonify(response.to_dict())

    except Exception as e:
        return jsonify({"error": str(e)}), 500

