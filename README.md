# CART498 (GenAI)
## Assignment 4 - Jungian Dream Interpreter

### Jungian Concepts in Prompt Engineering

For text interpretation, I instructed GPT-4o to act as a Jungian dream analyst. The system prompt explicitly references key Jungian concepts: archetypes (shadow, anima/animus, the self), symbolic interpretation, the collective unconscious, and individuation. 

For image generation, I used Stable Diffusion with a prompt that combines the user's dream description with Jungian keywords: "Jungian symbolism, dream-like, surreal, archetypal, unconscious imagery" This steers the visual output toward symbolic and psychological content rather than literal illustration.

### User Guide

1. **Input**: Describe your dream in as much detail as possible: emotions, people, settings, colors, and recurring symbols.
2. **Output**: The app generates two interpretations: a textual Jungian analysis identifying archetypes and symbolic meaning, plus a visual representation of the dream's psychological themes.
3. **Interaction**: Press Enter (without Shift) or click Interpret to submit.

### Reflection

The dual-API approach successfully integrates both objectives: GPT-4o interprets the dream through Jungian theory, while Stable Diffusion visualizes its archetypal content. GPT-4o directly engages with Jung's framework (archetypes, symbolism, individuation), making the analysis rigorous. Stable Diffusion provides fast, cost-efficient image generation with a naturally dreamlike aesthetic that suits Jungian symbolism.

A prompt enhancement with explicit Jungian keywords (archetypal, surreal, unconscious imagery) guides both models toward thematically coherent output. Importantly, using urllib instead of external HTTP libraries keeps dependencies minimal—only Flask, OpenAI, python-dotenv, and gunicorn are required. 