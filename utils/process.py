from pydub import AudioSegment
import streamlit as st
from io import BytesIO
import assemblyai as aai
import os

def preprocess(data):
    if data is not None:
        audio = AudioSegment.from_wav(BytesIO(data))
        audio.export("./temp/file.wav", format="wav")


def transcribe(lang):
    config = aai.TranscriptionConfig(language_code=lang)

    aai.settings.api_key = st.secrets["auth_key"]

    transcriber = aai.Transcriber()

    transcript = transcriber.transcribe("./temp/file.wav", config=config)


    return transcript.text


def main(data, lang):
    if data is not None:
        processed_data = preprocess(data)
        ans = transcribe(lang)
        return ans
 
