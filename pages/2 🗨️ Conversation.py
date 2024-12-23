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
st.title("🗨️ Conversation")


def readContextFromFile(filePath):
    try:
        with open(filePath, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        st.error(f"Arquivo {filePath} não encontrado.")
        return ""


# Load Context
conversationLLMBehavior = readContextFromFile('conversationLlmBehavior.txt')
conversationUserContext = readContextFromFile('conversationUserContext.txt')
beginnerExamplesUserContext = readContextFromFile(
    'benginnerExamplesConversationUserContext.txt')
preIntermediateExamplesUserContext = readContextFromFile(
    'preIntermediateExamplesConversationUserContext.txt')


def getResponseFromModel(model, message, history):
    messages = [
        {"role": "system", "content": conversationLLMBehavior},
        {"role": "user", "content": conversationUserContext},
        {"role": "user", "content": beginnerExamplesUserContext},
        {"role": "user", "content": preIntermediateExamplesUserContext},
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


def getChatResponseLlama3Versatile(message, history):
    return getResponseFromModel("llama-3.1-70b-versatile", message, history)


def getChatResponseLlama3_8192(message, history):
    return getResponseFromModel("llama3-70b-8192", message, history)


def getChatResponseMixtral(message, history):
    return getResponseFromModel("mixtral-8x7b-32768", message, history)


def getChatResponseGemma2(message, history):
    return getResponseFromModel("gemma2-9b-it", message, history)


def getChatResponseLlama3Groq(message, history):
    return getResponseFromModel("llama3-groq-70b-8192-tool-use-preview", message, history)


def main():
    # Initialize Prompt State
    if "conversation_prompt" not in st.session_state:
        st.session_state.conversation_prompt = ""

    # Initialize Responses State
    if "conversation_responses" not in st.session_state:
        st.session_state.conversation_responses = {
            "llama-3.1-70b-versatile": [],
            "llama3-70b-8192": [],
            "mixtral-8x7b-32768": [],
            "gemma2-9b-it": [],
            "llama3-groq-70b-8192-tool-use-preview": [],
        }
        st.session_state.selectedConversationModel = "llama-3.1-70b-versatile"

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
                st.session_state.conversation_prompt = transcription

        selectedModel = st.selectbox("Model", [
            "llama-3.1-70b-versatile",
            "llama3-70b-8192",
            "mixtral-8x7b-32768",
            "gemma2-9b-it",
            "llama3-groq-70b-8192-tool-use-preview",
        ])

        selectedVoice = st.selectbox("Accent", VOICES)

    st.session_state.selectedConversationModel = selectedModel

    st.write("Esse chatbot é especializado em conversas simples, seguindo um script comum de ensino. Também sugere expressões idiomáticas comuns e explica nuances linguísticas e culturais.")

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
    for userMessage, response in st.session_state.conversation_responses[selectedModel]:
        with st.chat_message("user"):
            st.write(f"{userMessage}")
        with st.chat_message("assistant"):
            st.write(f"{response}")

    # User Input for written
    newPrompt = st.chat_input("Digite uma mensagem")
    if newPrompt:
        st.session_state.conversation_prompt = newPrompt

    if st.session_state.conversation_prompt:
        # Models
        modelFunctions = {
            "llama-3.1-70b-versatile": getChatResponseLlama3Versatile,
            "llama3-70b-8192": getChatResponseLlama3_8192,
            "mixtral-8x7b-32768": getChatResponseMixtral,
            "gemma2-9b-it": getChatResponseGemma2,
            "llama3-groq-70b-8192-tool-use-preview": getChatResponseLlama3Groq,
        }
        response = modelFunctions[selectedModel](
            st.session_state.conversation_prompt, st.session_state.conversation_responses[selectedModel])

        # Add to the historic
        st.session_state.conversation_responses[selectedModel].append(
            (st.session_state.conversation_prompt, response))

        # Show answer
        with st.chat_message("user"):
            st.write(f"{st.session_state.conversation_prompt}")
            st.session_state.conversation_prompt = ""

            # Check if there is some record user audio
            if 'audioBytes' in st.session_state and st.session_state.audioBytes:
                st.audio(st.session_state.audioBytes, format="audio/wav")

        with st.chat_message("assistant"):
            st.write(f"{response}")
            generateAndDisplayAudio(str(response), selectedVoice)


if __name__ == "__main__":
    main()
