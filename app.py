from flask import Flask, render_template, request
import openai
import os
import json
import urllib.request
from collections import OrderedDict
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
stability_key = os.getenv("STABILITY_API_KEY")

IMAGE_WIDTH = 768
IMAGE_HEIGHT = 768
IMAGE_STEPS = 20
IMAGE_CFG_SCALE = 6.5
IMAGE_TIMEOUT = 20
IMAGE_PROMPT_MAX_CHARS = 400
IMAGE_CACHE_MAX = 32
_image_cache = OrderedDict()

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

def _get_cached_image(key):
    if key in _image_cache:
        _image_cache.move_to_end(key)
        return _image_cache[key]
    return None

def _set_cached_image(key, value):
    _image_cache[key] = value
    _image_cache.move_to_end(key)
    if len(_image_cache) > IMAGE_CACHE_MAX:
        _image_cache.popitem(last=False)

def fetch_dream_image(dream):
    """Generate dream visualization with Stable Diffusion using urllib."""
    if not stability_key:
        return None

    cache_key = dream.strip().lower()
    cached = _get_cached_image(cache_key)
    if cached:
        return cached

    try:
        url = "https://api.stability.ai/v1/generate"
        headers = {
            "authorization": f"Bearer {stability_key}",
            "content-type": "application/json",
        }
        trimmed_dream = dream.strip()[:IMAGE_PROMPT_MAX_CHARS]
        payload = {
            "text_prompts": [{
                "text": f"{trimmed_dream}, Jungian symbolism, dream-like, surreal, archetypal, unconscious imagery"
            }],
            "cfg_scale": IMAGE_CFG_SCALE,
            "height": IMAGE_HEIGHT,
            "width": IMAGE_WIDTH,
            "samples": 1,
            "steps": IMAGE_STEPS,
        }
        
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=IMAGE_TIMEOUT) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        if "artifacts" in data and len(data["artifacts"]) > 0:
            result = f"data:image/png;base64,{data['artifacts'][0]['base64']}"
            _set_cached_image(cache_key, result)
            return result
    except Exception as e:
        print(f"Image generation error: {e}")
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
