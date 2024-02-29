import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI()
client.api_key = OPENAI_API_KEY

def generate_response(prompt):
    completion = OpenAI().chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )

    if completion.choices[0].message is not None:
        return completion.choices[0].message.content
    else:
        return None

def audio_out(prompt):
    response = generate_response(prompt)
    speech_file_path = Path(__file__).parent / "output.mp3"
    output = OpenAI().audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=response
    )
    output.stream_to_file(speech_file_path)

def do_the_thing():
    audio_file = open("input.mp3", "rb")
    transcription = OpenAI().audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    audio_file.close()
    prompt = transcription.text
    audio_out(prompt)

do_the_thing()
