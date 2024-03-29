import ollama
import streamlit as st
import os
from utils import save_chat_history,load_chat_history_json,get_timestamp
from datetime import datetime
from streamlit_mic_recorder import mic_recorder
from transformers import pipeline
import yaml
import torch
from audio_transcribe import transcribe_audio

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

with open('style.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

def create_new_chat():
    st.session_state["session_key"] = "new_session"
    del st.session_state["messages"]
    st.session_state["messages"] = []

def load_chat():
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def set_session_name(session):
    st.session_state.session_key = session
    del st.session_state["messages"]
    st.session_state["messages"] = load_chat_history_json(session)

def model_res_generator():
    stream = ollama.chat(
        model=st.session_state["model"],
        messages=st.session_state["messages"],
        stream=True,
    )
    for chunk in stream:
        yield chunk["message"]["content"]

st.title("Knowly")
st.sidebar.title("Chat sessions")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "model" not in st.session_state:
    st.session_state["model"] = ""

if "session_key" not in st.session_state:
    if len(os.listdir('sessions/')) != 0:
        st.session_state["session_key"] = os.listdir('sessions/')[-1]
        st.session_state["messages"] = load_chat_history_json(st.session_state.session_key)
    else:
        st.session_state["session_key"] = "new_session"

def save_session(session_key):
    if "messages" in st.session_state:
        if st.session_state.session_key == "new_session":
            st.session_state.session_key = get_timestamp() + '.json'
            save_chat_history(st.session_state['messages'],st.session_state.session_key)
        else:
            save_chat_history(st.session_state['messages'],st.session_state.session_key)

models = [model["name"] for model in ollama.list()["models"]]
st.session_state["model"] = st.selectbox("choose you model", models)

load_chat()

voice_recording = mic_recorder(start_prompt="Start recording", stop_prompt="Stop recording", just_once=True)
transcribed_audio_prompt = ''
if voice_recording:
        transcribed_audio_prompt = transcribe_audio(voice_recording["bytes"])
        
user_prompt = st.chat_input("Enter your question:")
if user_prompt is not None or transcribed_audio_prompt != '':
    if user_prompt:
        prompt = user_prompt
    else:
        prompt = transcribed_audio_prompt
        
    st.session_state["messages"].append({"role" : "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message = st.write_stream(model_res_generator())
        st.session_state["messages"].append({"role":"assistant", "content" : message})

save_session(st.session_state.session_key)

st.sidebar.button(label="new chat", on_click=create_new_chat)

session_list = os.listdir("sessions/")
for session in session_list:
    st.sidebar.button(label=session,use_container_width=True,on_click=set_session_name, args=[session])