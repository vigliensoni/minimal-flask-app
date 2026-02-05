from flask import Flask, render_template, request, Response, abort, url_for
from openai import OpenAI
import os
import base64
import uuid
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Use the modern OpenAI client once (and set a timeout so calls don’t hang forever)
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    timeout=120,  # seconds
)

# Very simple in-memory image store (good enough for a minimal app)
# Note: this will reset on deploy/restart, which is fine for a demo.
IMAGE_STORE = {}  # id -> {"bytes": ..., "mime": ...}

@app.route("/image/<img_id>")
def serve_image(img_id: str):
    item = IMAGE_STORE.get(img_id)
    if not item:
        abort(404)
    return Response(item["bytes"], mimetype=item["mime"])

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    image_url = None

    if request.method == "POST":
        prompt = request.form.get("prompt", "").strip()
        if not prompt:
            return render_template("index.html", result="Error: empty prompt", image_url=None)

        try:
            # Text
            response = client.responses.create(
                model="gpt-4.1-mini",
                input=[
                    {"role": "developer", "content": "You are a psychedelic AI that speaks in Oulipian constraints. Respond with surreal language."},
                    {"role": "user", "content": prompt},
                ],
                temperature=1.0,
                max_output_tokens=100,
            )
            result = response.output_text

            image_prompt = (
                f"Create a hyperrealistic photographic collage inspired by the question: '{prompt}' "
                f"and the response: '{result}'. Be inspired by Max Ernst, Hannah Höch, and other artists "
                f"that developed collage as a way to create illusionistic and surreal compositions. "
                f"Hyperrealistic photography, intricate details, dramatic lighting, 8k resolution."
            )

            # Image
            image_response = client.images.generate(
                model="gpt-image-1-mini",
                prompt=image_prompt,
                size="auto",
                quality="low",
                n=1,
            )

            image_data = image_response.data[0]

            if getattr(image_data, "url", None):
                # If the API gives you a URL, use it directly (small HTML)
                image_url = image_data.url

            elif getattr(image_data, "b64_json", None):
                # Decode base64 and serve from our own /image/<id> endpoint (small HTML)
                img_bytes = base64.b64decode(image_data.b64_json)

                # If you know it’s JPEG you can keep this; otherwise you can sniff it.
                mime = "image/jpeg"

                img_id = uuid.uuid4().hex
                IMAGE_STORE[img_id] = {"bytes": img_bytes, "mime": mime}

                image_url = url_for("serve_image", img_id=img_id)

        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template("index.html", result=result, image_url=image_url)

if __name__ == "__main__":
    app.run(debug=True)