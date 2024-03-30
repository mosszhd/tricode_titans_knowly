import os
import yaml
from datetime import datetime

import ollama
import torch
import streamlit as st
from transformers import pipeline
from streamlit_mic_recorder import mic_recorder
from utils import save_chat_history, load_chat_history_json, get_timestamp

from prompt_templates import SYSTEM_PROMPT
from audio_transcribe import transcribe_audio
from text_processor import get_document_chunks
from chromadb_operations import ChromadbOperations

header = st.container()
header.title("Knowly")
header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)

with header:
    col1, col2 = st.columns(2)
    with col1:
        if "model" not in st.session_state:
            st.session_state["model"] = ""
        models = [model["name"] for model in ollama.list()["models"]]
        st.session_state["model"] = st.selectbox("Choose your model", models)
    with col2:
        st.write('Record Audio:')
        voice_recording = mic_recorder(start_prompt="Start recording", stop_prompt="Stop recording", just_once=True)
        transcribed_audio_prompt = ''
        if voice_recording:
            transcribed_audio_prompt = transcribe_audio(voice_recording["bytes"])

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

def model_res_generator(rag:bool=False):
    prompt = st.session_state["messages"][-1]["content"]  # extracting last user prompt
    if rag:
        context = st.session_state["vector_db"].query(query_text=prompt, k=1)  # fetching similar contexts from vector database

        # creating paragraph of contexts
        paragraph = ""
        for i, item in enumerate(context):
            paragraph += item
            if i != len(context)-1:
                paragraph += "\n"
        
        # replacing user prompt with augmented prompt
        st.session_state["messages"][-1]["content"] = formatted_prompt(query=prompt, context=paragraph)
    
    stream = ollama.chat(
        model=st.session_state["model"],
        messages=st.session_state["messages"],
        stream=True,
    )

    # replacing augmented prompt with actual user prompt
    if rag:
        st.session_state["messages"][-1]["content"] = prompt
    for chunk in stream:
        yield chunk["message"]["content"]

def formatted_prompt(query:str, context:str):
    return SYSTEM_PROMPT + f"Question: {query}" + f"\n\nContext: {context}"

def save_session(session_key):
    if "messages" in st.session_state:
        if st.session_state.session_key == "new_session":
            st.session_state.session_key = get_timestamp() + '.json'
            save_chat_history(st.session_state['messages'], st.session_state.session_key)
        else:
            save_chat_history(st.session_state['messages'], st.session_state.session_key)

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "session_key" not in st.session_state:
    if len(os.listdir('sessions/')) != 0:
        st.session_state["session_key"] = os.listdir('sessions/')[-1]
        st.session_state["messages"] = load_chat_history_json(st.session_state.session_key)
    else:
        st.session_state["session_key"] = "new_session"

load_chat()

with st.sidebar:
    st.sidebar.write('**Pdf Upload:**')
    with st.form("my-form", clear_on_submit=True):
        uploaded_docs = st.file_uploader(label="Upload pdf or text files",
                                         accept_multiple_files=True,
                                         key="document_uploader",
                                         type=["pdf"])
        submitted = st.form_submit_button("UPLOAD")

    if submitted:
        print("uploaded docs section is running...")
        os.makedirs("docs", exist_ok=True)
        with st.spinner("Processing documents..."):
            # saving the uploaded files in directory
            for file_item in uploaded_docs:
                with open(f"docs/{file_item.name}", "wb") as f:
                    f.write(file_item.getbuffer())
                f.close()
        
        st.session_state["vector_db"] = ChromadbOperations()
        text_chunks = get_document_chunks(path="docs")
        st.session_state["vector_db"].insert_data(text_chunks)
        del st.session_state["document_uploader"]

        # deleting currently uploaded pdfs
        for file_item in uploaded_docs:
            if file_item.name in os.listdir(str(os.getcwd())+"/docs"):
                os.remove(f"docs/{file_item.name}")

# pdf chat
pdf_chat_mode = st.sidebar.toggle(label="PDF Chat",
                                  key="pdf_chat",
                                  value=False,
                                  disabled=True if "vectorstore" not in os.listdir(str(os.getcwd())) else False)

# load the current vector database if exists
if pdf_chat_mode:
    if "vector_db" not in st.session_state.keys() and "vectorstore" in os.listdir(str(os.getcwd())):
        st.session_state["vector_db"] = ChromadbOperations()

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
        message = st.write_stream(model_res_generator(rag=pdf_chat_mode))
        st.session_state["messages"].append({"role": "assistant", "content": message})

save_session(st.session_state.session_key)

st.sidebar.write('**Chat History:**')

st.sidebar.button(label="New chat", on_click=create_new_chat)

session_list = os.listdir("sessions/")
for session in session_list:
    st.sidebar.button(label=session,use_container_width=True,on_click=set_session_name, args=[session])