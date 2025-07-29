
# EvilWormGPT

**EvilWormGPT** is a lightweight Python wrapper for a twisted, sarcastic AI chatbot API that behaves like a villain.

## Features

- Keeps a conversation history
- Sends requests to a publicly exposed evil AI endpoint
- Returns hostile, funny, or unexpected replies

## Installation

```bash
pip install evilwormgpt
```

## Usage

```python
from evilworm import EvilWorm

bot = EvilWorm()
reply = bot.ask("Who created you?")
print("AI:", reply)
```

## Reset Chat

```python
bot.reset()
```

## Warning

This library interacts with an experimental and intentionally rude chatbot. Use responsibly and for fun purposes only.
