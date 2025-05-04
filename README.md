## LlamaCon Hackathon 2025

## Idea

see.fm - radio podcast about what I'm seeing

- phone camera or dash cam updates image in cloud periodically
- call llama API (Llama-4-Maverick-17B-128E-Instruct-FP8) to generate conversation about the image
- use PlayAI to speak the conversation with natural voices

## Run

env expected:

LLAMA_API_KEY
PLAYHT_USER_ID
PLAYHT_API_KEY

`python3 play_main.py`

Currently using preset image URL.

