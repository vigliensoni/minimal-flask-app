from flask import Flask, render_template, request
import openai
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

async def fetch_dream_interpretation(dream):
    """Generate Jungian dream interpretation."""
    return await asyncio.to_thread(
        lambda: openai.chat.completions.create(
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
    )

async def fetch_dream_image(dream):
    """Generate dream visualization with Stable Diffusion."""
    import requests
    return await asyncio.to_thread(
        lambda: requests.post(
            "https://api.stability.ai/v1/generate",
            headers={
                "authorization": f"Bearer {os.getenv('STABILITY_API_KEY')}",
                "content-type": "application/json",
            },
            json={
                "text_prompts": [{"text": dream + ", Jungian symbolism, dream-like, surreal, archetypal"}],
                "cfg_scale": 7,
                "height": 1024,
                "width": 1024,
                "samples": 1,
                "steps": 30,
            },
        ).json()
    

@app.route("/", methods=["GET", "POST"])
async def index():
    result = None
    if request.method == "POST":
        dream = request.form["prompt"]
        try:
            interpretation_task = fetch_dream_interpretation(dream)
            image_task = fetch_dream_image(dream)
            interpretation, image = await asyncio.gather(interpretation_task, image_task)
            result = [interpretation.choices[0].message.content, image.data[0].url]
        except Exception as e:
            result = [f"Error: {str(e)}"]
    return render_template("index.html", result=result)

if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    app.run(debug=True)