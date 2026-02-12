# CART498 (GenAI)
## Assignment 4 - Jungian Dream Interpreter

### Jungian Concepts in Prompt Engineering

For text interpretation, I instructed GPT-4o to act as a Jungian dream analyst. The system prompt explicitly references key Jungian concepts: archetypes (shadow, anima/animus, the self), symbolic interpretation, the collective unconscious, and individuation. The model structures responses into three sections—Symbols, Archetypal Themes, and Psychological Message—mirroring clinical dream analysis methodology.

For image generation, I used DALL-E 3 with a prompt that combines the user's dream description with Jungian keywords: "Jungian symbolism, dream-like, surreal, archetypal, unconscious imagery." This steers the visual output toward symbolic and psychological content rather than literal illustration.

### User Guide

1. **Input**: Describe your dream in as much detail as possible—emotions, people, settings, colors, and recurring symbols.
2. **Output**: The app generates two interpretations: a textual Jungian analysis identifying archetypes and symbolic meaning, plus a visual representation of the dream's psychological themes.
3. **Interaction**: Press Enter (without Shift) or click Interpret to submit.

### Reflection

The dual-API approach successfully integrates both objectives: GPT-4o interprets the dream through Jungian theory, while DALL-E 3 visualizes its archetypal content. The text interpretation directly engages with Jung's framework, making the analysis more rigorous than stylistic steering alone.

Challenges included ensuring DALL-E 3's images matched the dream's psychological themes rather than generating purely surreal visuals. The prompt enhancement with explicit Jungian keywords improved thematic coherence.

Future improvements could include extracting archetypal keywords from the interpretation to feed into image prompts, or allowing users to explore which archetypes dominate their recurring dreams.