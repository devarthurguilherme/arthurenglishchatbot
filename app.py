import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from utils import *
from audio_recorder_streamlit import audio_recorder
from EdgeAvailableVoices import VOICES
from UserInputLanguage import INPUT_LANGUAGE


# Carregar variáveis de ambiente
load_dotenv(override=True)

# Configurar cliente Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def readContextFromFile(file_path):
    # Função para ler o conteúdo do arquivo de contexto
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        st.error(f"Arquivo {file_path} não encontrado.")
        return ""


# Carregar o contexto
generalInstructions = readContextFromFile('instructions.txt')


def get_response_from_model(model, message, history):
    # Função genérica para chamada da API
    messages = [
        {"role": "user", "content": generalInstructions},
        # {"role": "user", "content": aboutTable}
    ]

    for msg in history:
        messages.append({"role": "user", "content": str(msg[0])})
        messages.append({"role": "assistant", "content": str(msg[1])})

    messages.append({"role": "user", "content": str(message)})

    response_content = ''
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
            response_content += content

    return response_content.strip()

# Funções específicas para cada modelo


def chat_groq_model_1(message, history):
    return get_response_from_model("gemma2-9b-it", message, history)


def chat_groq_model_2(message, history):
    return get_response_from_model("llama-3.1-70b-versatile", message, history)


def chat_groq_model_3(message, history):
    return get_response_from_model("llama3-groq-70b-8192-tool-use-preview", message, history)


def chat_groq_model_4(message, history):
    return get_response_from_model("llama3-70b-8192", message, history)


def chat_groq_mixtral(message, history):
    return get_response_from_model("mixtral-8x7b-32768", message, history)


def main():
    st.set_page_config(layout='wide')

    # Prompt State Started
    if "prompt" not in st.session_state:
        st.session_state.prompt = ""

    # Sidebar
    with st.sidebar:
        st.title("English Teacher Chatbot")

        # Button to start recording
        audio_bytes = audio_recorder()

        # Seleção da Lingua de User Input Audio
        selected_language = st.selectbox(
            "Input Audio Language", INPUT_LANGUAGE)

        if audio_bytes:
            # Convert audio bytes to a BytesIO object
            audio_buffer = io.BytesIO(audio_bytes)

            # Transcribe the audio
            transcription = transcribe_audio(audio_buffer, selected_language)

            # Show the transcription result
            # st.write(f"Transcribed text: {transcription}")

            if transcription:
                st.session_state.prompt = transcription

        # Inicializar o histórico do estado da sessão, se não existir
        if "responses" not in st.session_state:
            st.session_state.responses = {
                "gemma2-9b-it": [],
                "llama-3.1-70b-versatile": [],
                "llama3-groq-70b-8192-tool-use-preview": [],
                "llama3-70b-8192": [],
                "mixtral-8x7b-32768": []
            }
            st.session_state.selected_model = "gemma2-9b-it"

        # Seleção do modelo
        selected_model = st.selectbox("Model",
                                      ["gemma2-9b-it", "llama-3.1-70b-versatile", "llama3-groq-70b-8192-tool-use-preview", "llama3-70b-8192", "mixtral-8x7b-32768"])

        selected_voice = st.selectbox("Accent", VOICES)

    st.session_state.selected_model = selected_model

    # Exibir histórico com ícones
    st.write("**Chat:**")
    for user_message, response in st.session_state.responses[selected_model]:
        with st.chat_message("user"):
            st.write(f"{user_message}")
        with st.chat_message("assistant"):
            st.write(f"{response}")

    # Entrada do usuário
    newPrompt = st.chat_input("Digite uma mensagem")
    if newPrompt:
        st.session_state.prompt = newPrompt

    if st.session_state.prompt:
        # Funções do modelo
        model_functions = {
            "gemma2-9b-it": chat_groq_model_1,
            "llama-3.1-70b-versatile": chat_groq_model_2,
            "llama3-groq-70b-8192-tool-use-preview": chat_groq_model_3,
            "llama3-70b-8192": chat_groq_model_4,
            "mixtral-8x7b-32768": chat_groq_mixtral
        }
        response = model_functions[selected_model](
            st.session_state.prompt, st.session_state.responses[selected_model])

        # Adiciona ao histórico
        st.session_state.responses[selected_model].append(
            (st.session_state.prompt, response))

        # Exibe a resposta
        with st.chat_message("user"):
            st.write(f"{st.session_state.prompt}")
            # After sent, clean prompt message
            st.session_state.prompt = ""

            # Verifica se há áudio gravado
            if 'audio_bytes' in st.session_state and st.session_state.audio_bytes:
                # Exibe o áudio gravado se disponível
                st.audio(st.session_state.audio_bytes, format="audio/wav")

        with st.chat_message("assistant"):
            st.write(f"{response}")
            generateAndDisplay_audio(str(response), selected_voice)


if __name__ == "__main__":
    main()
