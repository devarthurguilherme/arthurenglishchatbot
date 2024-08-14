import asyncio
import edge_tts
import streamlit as st
import tempfile
import shutil

# Lista de vozes disponíveis
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

st.title("Text-to-Speech with Edge TTS WAV")

# Área de entrada de texto
text = st.text_area("Enter the text to convert to speech")

# Dropdown para selecionar a voz
voice = st.selectbox("Select a voice", VOICES)

# Botão para gerar áudio
if st.button("Generate Audio"):
    if text.strip() == "":
        st.error("Please enter some text.")
    else:
        # Gera áudio de forma assíncrona
        audio_file_path = asyncio.run(generate_audio(text, voice))

        # Exibe o áudio
        st.audio(audio_file_path, format='audio/wav')

        # Remove o arquivo temporário após o uso
        shutil.os.remove(audio_file_path)
