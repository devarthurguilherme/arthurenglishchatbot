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

# Config Client
client = Groq(api_key=os.environ.get("GROQ_API_KEY3"))


def readContextFromFile(filePath):
    try:
        with open(filePath, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        st.error(f"Arquivo {filePath} não encontrado.")
        return ""


# Load Context
llmBehavior = readContextFromFile('llmBehavior.txt')
userContext = readContextFromFile('userContext.txt')


def getResponseFromModel(model, message, history):
    messages = [
        {"role": "system", "content": llmBehavior},
        {"role": "user", "content": userContext},
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
def chatLlama3_1_70bVersatile(message, history):
    return getResponseFromModel("llama-3.1-70b-versatile", message, history)


def chatLlama3_70b_8192(message, history):
    return getResponseFromModel("llama3-70b-8192", message, history)


def chatGroqMixtral(message, history):
    return getResponseFromModel("mixtral-8x7b-32768", message, history)


def chatGemma2_9bIt(message, history):
    return getResponseFromModel("gemma2-9b-it", message, history)


def chatLlama3Groq_70b_8192ToolUsePreview(message, history):
    return getResponseFromModel("llama3-groq-70b-8192-tool-use-preview", message, history)


def main():
    st.set_page_config(layout='wide')

    # Prompt State Started
    if "prompt" not in st.session_state:
        st.session_state.prompt = ""

    # Sidebar
    with st.sidebar:
        st.title("English Teacher Chatbot")

        # Button to start recording
        audioBytes = audio_recorder()

        # Select Language to User Input Audio
        selectedLanguage = st.selectbox(
            "Input Audio Language", INPUT_LANGUAGE)

        if audioBytes:
            audioBuffer = io.BytesIO(audioBytes)
            transcription = transcribeAudio(audioBuffer, selectedLanguage)

            if transcription:
                st.session_state.prompt = transcription

        if "responses" not in st.session_state:
            st.session_state.responses = {
                "llama-3.1-70b-versatile": [],
                "llama3-70b-8192": [],
                "mixtral-8x7b-32768": [],
                "gemma2-9b-it": [],
                "llama3-groq-70b-8192-tool-use-preview": [],
            }
            st.session_state.selectedModel = "llama-3.1-70b-versatile"

        selectedModel = st.selectbox("Model", [
            "llama-3.1-70b-versatile",
            "llama3-70b-8192",
            "mixtral-8x7b-32768",
            "gemma2-9b-it",
            "llama3-groq-70b-8192-tool-use-preview",
        ])

        selectedVoice = st.selectbox("Accent", VOICES)

    st.session_state.selectedModel = selectedModel

    # Show Historic Chat
    st.write("**Chat:**")
    for userMessage, response in st.session_state.responses[selectedModel]:
        with st.chat_message("user"):
            st.write(f"{userMessage}")
        with st.chat_message("assistant"):
            st.write(f"{response}")

    # User Input for written
    newPrompt = st.chat_input("Digite uma mensagem")
    if newPrompt:
        st.session_state.prompt = newPrompt

    if st.session_state.prompt:
        # Models
        modelFunctions = {
            "llama-3.1-70b-versatile": chatLlama3_1_70bVersatile,
            "llama3-70b-8192": chatLlama3_70b_8192,
            "mixtral-8x7b-32768": chatGroqMixtral,
            "gemma2-9b-it": chatGemma2_9bIt,
            "llama3-groq-70b-8192-tool-use-preview": chatLlama3Groq_70b_8192ToolUsePreview,
        }
        response = modelFunctions[selectedModel](
            st.session_state.prompt, st.session_state.responses[selectedModel])

        # Add to the historic
        st.session_state.responses[selectedModel].append(
            (st.session_state.prompt, response))

        # Show answer
        with st.chat_message("user"):
            st.write(f"{st.session_state.prompt}")
            st.session_state.prompt = ""

            # Check if there is some record user audio
            if 'audioBytes' in st.session_state and st.session_state.audioBytes:
                st.audio(st.session_state.audioBytes, format="audio/wav")

        with st.chat_message("assistant"):
            st.write(f"{response}")
            generateAndDisplayAudio(str(response), selectedVoice)


if __name__ == "__main__":
    main()
