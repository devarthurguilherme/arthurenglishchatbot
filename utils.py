import asyncio
import edge_tts
import streamlit as st
import tempfile
import speech_recognition as sr
import re
import io


async def generateAudio(text, voice):
    # Create a new temporary file to save audio
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tempFile:
        tempFilePath = tempFile.name
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(tempFilePath)

    # Return temp audio path
    return tempFilePath


def cleanText(text):
    # use a regex to keep just letters and numbers
    cleanedText = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return cleanedText


def generateAndDisplayAudio(text, voice):
    # Clean text to remove special characters
    cleanedText = cleanText(text)

    # Execute generate audio async way
    audioFilePath = asyncio.run(generateAudio(cleanedText, voice))

    # Show audio in the Streamlit Display
    st.audio(audioFilePath, format='audio/wav')


def transcribeAudio(audioBuffer, language='en-US'):
    # Transform record audio in text using SpeechRecognition Library

    # Start Reconizer
    recognizer = sr.Recognizer()
    with sr.AudioFile(audioBuffer) as source:
        audioData = recognizer.record(source)
        try:
            # Make recognition as chosen idiom
            text = recognizer.recognize_google(audioData, language=language)
            return text
        except sr.RequestError as e:
            return f"Could not request results; {e}"
        except sr.UnknownValueError:
            return "Something happened! Maybe audio doesn't work or something like that!"
