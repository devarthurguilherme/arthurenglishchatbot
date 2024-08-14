import asyncio
import edge_tts
import streamlit as st
import tempfile
import speech_recognition as sr

import io

VOICES = ['en-US-GuyNeural', 'en-US-JennyNeural']


async def generate_audio(text, voice):
    """Gera um arquivo de áudio a partir do texto usando a voz selecionada e salva como WAV."""
    # Cria um arquivo temporário para salvar o áudio
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
        temp_file_path = temp_file.name
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(temp_file_path)

    # Retorna o caminho do arquivo temporário
    return temp_file_path


def generateAndDisplay_audio(text, voice):
    """Gera áudio a partir do texto e exibe o áudio em Streamlit."""
    # Executa a geração de áudio de forma assíncrona
    audio_file_path = asyncio.run(generate_audio(text, voice))

    # Exibe o áudio em Streamlit
    st.audio(audio_file_path, format='audio/mp3')


def transcribe_audio(audio_buffer):
    # Initialize recognizer
    r = sr.Recognizer()
    with sr.AudioFile(audio_buffer) as source:
        audio_data = r.record(source)
        try:
            # Perform speech recognition
            text = r.recognize_google(audio_data, language='pt-BR')
            return text
        except sr.RequestError as e:
            return f"Could not request results; {e}"
        except sr.UnknownValueError:
            return "Unknown error occurred"
