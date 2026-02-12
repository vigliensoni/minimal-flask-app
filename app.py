from flask import Flask, render_template, request
import openai
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
stability_key = os.getenv("STABILITY_API_KEY")

def fetch_dream_interpretation(dream):
    """Generate Jungian dream interpretation with GPT-4o."""
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "developer",
                "content": """You are a Jungian dream analyst. Interpret dreams using:
- Archetypes (shadow, anima/animus, self, wise old man/woman, etc.)
- Symbolic meaning of objects, people, and settings
- Connection to the collective unconscious
- What the dream reveals about individuation and psychological growth
Structure your response with clear sections: Symbols, Archetypal Themes, and Psychological Message. Be concise."""
            },
            {"role": "user", "content": dream}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content

def fetch_dream_image(dream):
    """Generate dream visualization with Stable Diffusion."""
    response = requests.post(
        "https://api.stability.ai/v1/generate",
        headers={
            "authorization": f"Bearer {stability_key}",
            "content-type": "application/json",
        },
        json={
            "text_prompts": [{"text": dream + ", Jungian symbolism, dream-like, surreal, archetypal, unconscious imagery"}],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30,
        },
    )
    data = response.json()
    if "artifacts" in data and len(data["artifacts"]) > 0:
        return f"data:image/png;base64,{data['artifacts'][0]['base64']}"
    return None

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        dream = request.form["prompt"]
        try:
            interpretation = fetch_dream_interpretation(dream)
            image = fetch_dream_image(dream)
            result = [interpretation, image]
        except Exception as e:
            result = [f"Error: {str(e)}"]
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)