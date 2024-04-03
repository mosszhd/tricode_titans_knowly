import json
from datetime import datetime
import ollama
import streamlit as st
import yaml
import re
from prompt_templates import SUMMARY_PROMPT


with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

session_dir = config["session_path"]

def save_chat_history(chat_history, session_key):
    file_name = f"{session_dir}/{session_key}"
    with open(file_name, "w") as f:
        json.dump(chat_history, f)

def load_chat_history_json(session_name):
    filename = f"{session_dir}/{session_name}"
    with open(filename, "r") as f:
        json_data = json.load(f)
    return json_data
    
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

def create_new_chat():
    if "message_count" in st.session_state.keys():
        st.session_state["message_count"] = 0   # resetting the message count
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

def save_session():
    if st.session_state["message_count"] == 1 and st.session_state.session_key == "new_session":
        # when user creates a new session and has at least one interaction then generate title
        st.session_state["selected_chat"] = format_chat_title(get_summary())
    if "messages" in st.session_state:
        if st.session_state.session_key == "new_session":
            st.session_state.session_key = st.session_state["selected_chat"] + '.json'
            save_chat_history(st.session_state['messages'], st.session_state.session_key)
        else:
            save_chat_history(st.session_state['messages'], st.session_state.session_key)
            
def get_summary():
    st.session_state["messages"].append({'role': 'system', 'content': SUMMARY_PROMPT})
    response = ollama.chat(model=st.session_state["model"], 
                           messages=st.session_state["messages"])
    st.session_state["messages"].pop()  # removing the last system message which is the Summary prompt
    return response["message"]["content"]
    
def format_chat_title(text:str):
    text = re.sub(r'\.\w+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = text.replace(".json", "")
    return text[:30]