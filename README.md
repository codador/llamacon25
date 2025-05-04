## LlamaCon Hackathon 2025

## Idea

see.fm -- radio about what I'm seeing

- phone camera or dash cam updates image in cloud periodically
- call llama API (Llama-4-Maverick-17B-128E-Instruct-FP8) to generate conversation about the image
- use PlayAI to speak the conversation with natural voices

## Run

env expected:

```
LLAMA_API_KEY=
PLAYHT_USER_ID=
PLAYHT_API_KEY=
```

`python3 play_main.py`

Currently using preset image URL.

## Demo video:

https://www.loom.com/share/d96bd41f6d1e4804b26141b73bb2b8c2?sid=3b321f97-b7e4-48e3-9479-9abec310d7b9

