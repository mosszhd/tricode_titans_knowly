import os
import yaml
import ollama
import streamlit as st
from streamlit_mic_recorder import mic_recorder
from text_processor import get_document_chunks
from chromadb_operations import ChromadbOperations
from audio_transcribe import transcribe_audio
from image_handler import multimodal_response
from llm_response import model_res_generator
from utils import *


with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

header = st.container()
header.title("Knowly")
header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)

with header:
    col1, col2 = st.columns(2)
    with col1:
        if "model" not in st.session_state:
            st.session_state["model"] = ""
        models = [model["name"] for model in ollama.list()["models"]]
        
        st.session_state["model"] = config["model_map"][st.selectbox("Choose your model", config["models"])]
    with col2:
        st.write('Record Audio:')
        voice_recording = mic_recorder(start_prompt="Start recording", stop_prompt="Stop recording", just_once=True)
        transcribed_audio_prompt = ''
        if voice_recording:
            transcribed_audio_prompt = transcribe_audio(voice_recording["bytes"])
with open('style.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# initializing the message_count
if "message_count" not in st.session_state.keys():
    st.session_state["message_count"] = 0

if "session_key" not in st.session_state:
    os.makedirs(session_dir, exist_ok=True)
    if len(os.listdir(config["session_path"])) != 0:
        st.session_state["session_key"] = os.listdir(config["session_path"])[-1]
        st.session_state["messages"] = load_chat_history_json(st.session_state.session_key)
    else:
        st.session_state["session_key"] = "new_session"

load_chat()

with st.sidebar:
    # st.sidebar.write('**Pdf Upload:**')
    with st.form("pdf-form", clear_on_submit=True):
        uploaded_docs = st.file_uploader(label="Upload pdf files",
                                         accept_multiple_files=True,
                                         key="document_uploader",
                                         type=config["allowed_doc_formats"])
        submitted = st.form_submit_button("UPLOAD")

    if submitted:
        os.makedirs(config["pdf_path"], exist_ok=True)
        with st.spinner("Processing documents..."):
            # saving the uploaded files in directory
            save_dir = config["pdf_path"]
            for file_item in uploaded_docs:
                with open(f"{save_dir}/{file_item.name}", "wb") as f:
                    f.write(file_item.getbuffer())
                f.close()
        
        st.session_state["vector_db"] = ChromadbOperations()
        text_chunks = get_document_chunks(path=config["pdf_path"])
        st.session_state["vector_db"].insert_data(text_chunks)
        del st.session_state["document_uploader"]

        # deleting currently uploaded pdfs
        for file_item in uploaded_docs:
            if file_item.name in os.listdir(str(os.getcwd()) + "/" + config["pdf_path"]):
                os.remove(config["pdf_path"] + f"/{file_item.name}")

# pdf chat
pdf_chat_mode = st.sidebar.toggle(label="PDF Chat",
                                  key="pdf_chat",
                                  value=False,
                                  disabled=True if "vectorstore" not in os.listdir(str(os.getcwd())) else False)

# load the current vector database if exists
if pdf_chat_mode:
    if "vector_db" not in st.session_state.keys() and "vectorstore" in os.listdir(str(os.getcwd())):
        st.session_state["vector_db"] = ChromadbOperations()

# image upload
with st.sidebar:
    # st.sidebar.write('**Image Upload:**')
    with st.form("image-form", clear_on_submit=True):
        uploaded_image = st.file_uploader(label="Upload image file", 
                                          type=config["allowed_image_formats"])
        image_submitted = st.form_submit_button("UPLOAD")

    if image_submitted:
        os.makedirs(config["image_dir"], exist_ok=True)
        with st.spinner("Processing image..."):
            image_save_dir = config["image_dir"]
            with open(f"{image_save_dir}/{uploaded_image.name}", "wb") as f:
                f.write(uploaded_image.getbuffer())
            f.close()
            st.session_state["image_name"] = f"{image_save_dir}/{uploaded_image.name}"

# image chat
image_chat_mode = st.sidebar.toggle(label="Image Chat",
                                  key="image_chat",
                                  value=False,
                                  disabled=True if "image_name" not in st.session_state.keys() else False)

user_prompt = st.chat_input("Enter your question:")
if user_prompt is not None or transcribed_audio_prompt != '':
    st.session_state["message_count"] += 1   # increasing message count
    if user_prompt:
        prompt = user_prompt
    else:
        prompt = transcribed_audio_prompt
    
    st.session_state["messages"].append({"role" : "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if image_chat_mode:
            message = st.write_stream(multimodal_response(prompt=prompt, image_path=st.session_state["image_name"]))
        else:
            message = st.write_stream(model_res_generator(rag=pdf_chat_mode))
        st.session_state["messages"].append({"role": "assistant", "content": message})

if st.session_state["message_count"] > 0:
    save_session()

st.sidebar.write('**Chat History:**')
st.sidebar.button(label="New chat", on_click=create_new_chat)

session_list = [format_chat_title(chat_title) for chat_title in os.listdir(config["session_path"])]

for session in session_list:
    st.sidebar.button(label=session, use_container_width=True, on_click=set_session_name, args=[session])