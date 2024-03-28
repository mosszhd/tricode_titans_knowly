import ollama
import streamlit as st
import os
from utils import save_chat_history,load_chat_history_json,get_timestamp
from datetime import datetime
from streamlit_mic_recorder import mic_recorder

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

print(st.session_state.session_key)

load_chat()

#chatbox_column, recording_column= st.columns(2)

#with chatbox_column:
if prompt := st.chat_input("Enter your question:"):
    st.session_state["messages"].append({"role" : "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message = st.write_stream(model_res_generator())
        st.session_state["messages"].append({"role":"assistant", "content" : message})

# with recording_column:
#     st.button(label='hi')

save_session(st.session_state.session_key)

st.sidebar.button(label="new chat", on_click=create_new_chat)

session_list = os.listdir("sessions/")
for session in session_list:
    st.sidebar.button(label=session,use_container_width=True,on_click=set_session_name, args=[session])
