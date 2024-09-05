import io
import streamlit as st
import speech_recognition as sr
from audio_recorder_streamlit import audio_recorder


def transcribe_audio(audio_buffer, language="en"):
    # Initialize recognizer
    r = sr.Recognizer()
    with sr.AudioFile(audio_buffer) as source:
        audio_data = r.record(source)
        try:
            # Perform speech recognition
            text = r.recognize_google(audio_data, language=language)
            return text
        except sr.RequestError as e:
            return f"Could not request results; {e}"
        except sr.UnknownValueError:
            return "Unknown error occurred"


def main():
    st.title("🗣️ → 📖 Audio to Text")

    # Sidebar for language selection
    selectedLanguage = st.selectbox(
        "Input Audio Language", ["English", "Portuguese"]  # Example languages
    )

    # Button to start recording
    audio_bytes = audio_recorder()

    if audio_bytes:
        audio_buffer = io.BytesIO(audio_bytes)
        transcription = transcribe_audio(audio_buffer, selectedLanguage)

        # Show the transcription result
        st.write(f"Transcribed text: {transcription}")


if __name__ == "__main__":
    main()
