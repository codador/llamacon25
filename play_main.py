from pyht import Client
from dotenv import load_dotenv
from pyht.client import TTSOptions, Format
import os
load_dotenv()

import numpy as np
import sounddevice as sd
import simpleaudio as sa

import json
import requests

# Prompt LLM to generate script from image.

url = 'https://api.llama.com/v1/chat/completions'
llama_key = os.getenv("LLAMA_API_KEY")
headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {llama_key}'}
myobj = {
    "model": "Llama-4-Maverick-17B-128E-Instruct-FP8",
    "messages": [
      {
        "role": "user",
        "content": [
          {"type": "text", "text": "Create a conversation script between two people talking about this image, output only the spoken text, with each turn on a new line."},
          {
            "type": "image_url",
            "image_url": {
              "url": "https://codador.github.io/images/ferry1.jpg"
            }
          }
        ]
      }
    ],
    "max_tokens": 4096
}

x = requests.post(url, headers=headers, json=myobj)

print(x.text)
resp = json.loads(x.text)

text = resp['completion_message']['content']['text']

# Parse response to TTS-ready text.

turns = [x for x in text.splitlines() if x]
if not turns:
    exit()

lines = []
for turn in turns:
    if ':' in turn:
        _, line = turn.split(':', 1)
        lines.append(line.strip())
    else:
        lines.append(turn.strip())

for i in range(len(lines)):
    if lines[i][0] == '"' and lines[i][-1] == '"':
        lines[i] = lines[i][1:-1]

print(lines)

# TTS the text.

client = Client(
    user_id=os.getenv("PLAYHT_USER_ID"),
    api_key=os.getenv("PLAYHT_API_KEY"),
)

play_obj = None

voice1 = "s3://voice-cloning-zero-shot/baf1ef41-36b6-428c-9bdf-50ba54682bd8/original/manifest.json"
voice2 = "s3://voice-cloning-zero-shot/775ae416-49bb-4fb6-bd45-740f205d20a1/jennifersaad/manifest.json"

def play_line(line, id):
    global play_obj

    options = TTSOptions(voice=(voice1 if id & 1 else voice2), format=Format.FORMAT_WAV)
    response_chunks = []
    resp_bytes = b''
    print(line)
    j = 0
    for chunk in client.tts(line, options):
        if j == 0:
            with open('foo.wav', 'wb') as f:
                f.write(chunk)
        else:
            with open('foo.wav', 'ab') as f:
                f.write(chunk)
        j += 1

    print('done')

    wave_obj = sa.WaveObject.from_wave_file("foo.wav")
    if i > 0:
        play_obj.wait_done()
    play_obj = wave_obj.play()

for i, line in enumerate(lines):
    play_line(line, i)
if play_obj is not None:
    play_obj.wait_done()

client.close()


