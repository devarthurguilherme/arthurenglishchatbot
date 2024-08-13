import streamlit as st
from audio_recorder_streamlit import audio_recorder

audio_bytes = audio_recorder()
if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")

# from turtle import st
# from st_audiorec import st_audiorec # type: ignore

# wav_audio_data = st_audiorec()

# if wav_audio_data is not None:
#     st.audio(wav_audio_data, format='audio/wav')
