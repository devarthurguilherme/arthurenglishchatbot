import streamlit as st
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import io

# Function to transcribe audio from an in-memory WAV buffer


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


def main():
    st.title("Speech-to-Text Converter")

    # Button to start recording
    audio_bytes = audio_recorder()

    if audio_bytes:
        # Convert audio bytes to a BytesIO object
        audio_buffer = io.BytesIO(audio_bytes)

        # Transcribe the audio
        transcription = transcribe_audio(audio_buffer)

        # Show the transcription result
        st.write(f"Transcribed text: {transcription}")

        # Optionally, you can also play back the recorded audio
        st.audio(audio_bytes, format="audio/wav")


if __name__ == "__main__":
    main()
