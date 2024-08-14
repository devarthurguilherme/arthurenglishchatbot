import asyncio
import edge_tts
import streamlit as st
import tempfile

VOICES = ['en-US-GuyNeural', 'en-US-JennyNeural']


async def generate_audio(text, voice):
    # Create a temporary file to save the audio
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
        temp_file_path = temp_file.name
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(temp_file_path)

    # Return the path of the temporary file
    return temp_file_path

st.title("Text-to-Speech with Edge TTS")

# Input text area
text = st.text_area("Enter the text to convert to speech",
                    )

# Dropdown for selecting voice
voice = st.selectbox("Select a voice", VOICES)

# Button to generate audio
if st.button("Generate Audio"):
    # Generate audio asynchronously
    audio_file_path = asyncio.run(generate_audio(text, voice))

    # Display the audio
    st.audio(audio_file_path, format='audio/mp3')
