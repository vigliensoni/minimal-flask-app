# CART498 (GenAI)
## Assignment 4 - Jungian Dream Interpreter

This is a minimal Flask app that takes a dream description, generates a Jungian analysis with GPT-4o, and optionally renders a dream-like image using the Stability API.

**Entry Point**
`app.py`

## Setup

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Create a `.env` file with required API keys:

```bash
OPENAI_API_KEY=your_openai_key
STABILITY_API_KEY=your_stability_key
```

## Run

### Development (Flask built-in)

```bash
python app.py
```

The app will be available at `http://127.0.0.1:5000`.

### Production (Gunicorn)

```bash
gunicorn app:app
```

## Tests

There is no automated test suite in this repository yet. If you add tests later, include them under a `tests/` directory and document the command here (for example, `pytest`).

## Notes

- The Flask route is defined in `app.py`.
- The UI template lives at `templates/index.html`.
