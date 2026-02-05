from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")  # Securely load API key

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    image_url = None
    if request.method == "POST":
        prompt = request.form["prompt"]
        try:
            # Generate text response using GPT-4o-mini
            response = openai.responses.create(
                model="gpt-4.1-mini",  
                input=[
                    {"role": "developer", "content": "You are a psychedelic AI that speaks in Oulipian constraints. Respond with surreal language."}, 
                    {"role": "user", "content": prompt}
                ],
                temperature=1.0,
                max_output_tokens=100
            )
            result = response.output_text

            # Combine the question and response for image prompt
            image_prompt = f"Create a hyperrealistic photographic collage inspired by the question: '{prompt}' and the response: '{result}'. Be inspired by Max Ernst, Hannah Höch, and other artists that developed collage as a way to create illusionistic and surreal compositions. Hyperrealistic photography, intricate details, dramatic lighting, 8k resolution."
            
            # Generate image using OpenAI Image API
            image_response = openai.OpenAI().images.generate(
                model="gpt-image-1-mini",
                prompt=image_prompt,
                size="auto",
                quality="low",
                n=1,
            )
            image_data = image_response.data[0]
            if getattr(image_data, "url", None):
                image_url = image_data.url
            elif getattr(image_data, "b64_json", None):
                image_url = f"data:image/jpeg;base64,{image_data.b64_json}"
        except Exception as e:
            result = f"Error: {str(e)}"
    return render_template("index.html", result=result, image_url=image_url)

if __name__ == "__main__":
    app.run(debug=True)  # Run locally for testing
