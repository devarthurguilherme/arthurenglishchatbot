import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from utils import *
from audio_recorder_streamlit import audio_recorder
from EdgeAvailableVoices import VOICES
from UserInputLanguage import INPUT_LANGUAGE
import io

# Load Env Variables
load_dotenv(override=True)

GROC_API_KEY = os.getenv("GROC_API_KEY2")

# Config Client
client = Groq(
    api_key=GROC_API_KEY)

# Streamlit Configure here
st.set_page_config(page_title="Arthur's English Teacher 🤖",
                   page_icon="🤖", layout='wide')
st.title("🔄 From Portuguese to English")


def readContextFromFile(filePath):
    try:
        with open(filePath, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        st.error(f"Arquivo {filePath} não encontrado.")
        return ""


# Load Context
translateLLMBehavior = readContextFromFile('translateLlmBehavior.txt')
translateUserContext = readContextFromFile('translateUserContext.txt')


def getResponseFromModel(model, message, history):
    messages = [
        {"role": "system", "content": translateLLMBehavior},
        {"role": "user", "content": translateUserContext},
    ]

    for msg in history:
        messages.append({"role": "user", "content": str(msg[0])})
        messages.append({"role": "assistant", "content": str(msg[1])})

    messages.append({"role": "user", "content": str(message)})

    responseContent = ''
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.5,
        max_tokens=1024,
        top_p=0.65,
        stream=True,
        stop=None,
    )
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            responseContent += content

    return responseContent.strip()

# Functions to each model


def chatLlama3_3_70b_versatile(message, history):
    return getResponseFromModel("llama-3.3-70b-versatile", message, history)


def chatDeepseek_r1_distill_llama_70b(message, history):
    return getResponseFromModel("deepseek-r1-distill-llama-70b", message, history)


def chatQwen_2_5_coder_32b(message, history):
    return getResponseFromModel("qwen-2.5-coder-32b", message, history)


def chatGemma2_9b_it(message, history):
    return getResponseFromModel("gemma2-9b-it", message, history)


def chatMixtral_8x7b_32768(message, history):
    return getResponseFromModel("mixtral-8x7b-32768", message, history)


def main():
    # Initialize Prompt State
    if "translator_chat_prompt" not in st.session_state:
        st.session_state.translator_chat_prompt = ""

    # Initialize Responses State
    if "translator_chat_responses" not in st.session_state:
        st.session_state.translator_chat_responses = {
            "llama-3.3-70b-versatile": [],
            "deepseek-r1-distill-llama-70b": [],
            "qwen-2.5-coder-32b": [],
            "gemma2-9b-it": [],
            "mixtral-8x7b-32768": [],
        }
        st.session_state.selected_translator_model = "llama-3.1-70b-versatile"

    # Sidebar
    with st.sidebar:
        # Button to start recording
        audioBytes = audio_recorder()

        # Select Language to User Input Audio
        selectedLanguage = st.selectbox(
            "Input Audio Language", INPUT_LANGUAGE)

        if audioBytes:
            audioBuffer = io.BytesIO(audioBytes)
            transcription = transcribeAudio(audioBuffer, selectedLanguage)

            if transcription:
                st.session_state.translator_chat_prompt = transcription

        selectedModel = st.selectbox("Model", [
            "llama-3.3-70b-versatile",
            "deepseek-r1-distill-llama-70b",
            "qwen-2.5-coder-32b",
            "gemma2-9b-it",
            "mixtral-8x7b-32768",
        ])

        selectedVoice = st.selectbox("Accent", VOICES)

    st.session_state.selected_translator_model = selectedModel

    st.write("Esse chatbot é especializado em traduzir, adaptar e verificar a melhor expressão do Português para o Inglês.")

    # Adicionando uma divisória
    st.markdown("""
    <hr style="
        border: 0; 
        height: 0.5px; 
        background: #004080; 
        opacity: 0.2;
        margin-top: 5px; 
        margin-bottom: 20px;
    ">
    """, unsafe_allow_html=True)

    # Show Historic Chat
    st.write("**Chat:**")
    for userMessage, response in st.session_state.translator_chat_responses[selectedModel]:
        with st.chat_message("user"):
            st.write(f"{userMessage}")
        with st.chat_message("assistant"):
            st.write(f"{response}")

    # User Input for written
    newPrompt = st.chat_input("Digite uma mensagem")
    if newPrompt:
        st.session_state.translator_chat_prompt = newPrompt

    if st.session_state.translator_chat_prompt:
        # Models
        modelFunctions = {
            "llama-3.3-70b-versatile": chatLlama3_3_70b_versatile,
            "deepseek-r1-distill-llama-70b": chatDeepseek_r1_distill_llama_70b,
            "qwen-2.5-coder-32b": chatQwen_2_5_coder_32b,
            "gemma2-9b-it": chatGemma2_9b_it,
            "mixtral-8x7b-32768": chatMixtral_8x7b_32768,
        }
        response = modelFunctions[selectedModel](
            st.session_state.translator_chat_prompt, st.session_state.translator_chat_responses[selectedModel])

        # Add to the historic
        st.session_state.translator_chat_responses[selectedModel].append(
            (st.session_state.translator_chat_prompt, response))

        # Show answer
        with st.chat_message("user"):
            st.write(f"{st.session_state.translator_chat_prompt}")
            st.session_state.translator_chat_prompt = ""

            # Check if there is some record user audio
            if 'audioBytes' in st.session_state and st.session_state.audioBytes:
                st.audio(st.session_state.audioBytes, format="audio/wav")

        with st.chat_message("assistant"):
            st.write(f"{response}")
            generateAndDisplayAudio(str(response), selectedVoice)


if __name__ == "__main__":
    main()
