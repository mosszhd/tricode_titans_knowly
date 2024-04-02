import json
from datetime import datetime
import ollama
import streamlit as st
import yaml


with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

session_dir = config["session_path"]

def save_chat_history(chat_history,session_key, session_model):
    file_name = f"{session_dir}/{session_key}"
    chws = get_summary(chat_history, session_model)
    with open(file_name, "w") as f:
        json.dump(chws, f)

def load_chat_history_json(session_name):
    filename = f"{session_dir}/{session_name}"
    with open(filename, "r") as f:
        json_data = json.load(f)
    return json_data
    
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

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

def save_session(session_key):
    
    if "messages" in st.session_state:
        
        if st.session_state.session_key == "new_session":
            st.session_state.session_key = get_timestamp() + '.json'
            save_chat_history(st.session_state['messages'], st.session_state.session_key, st.session_state['model'])
        else:
            save_chat_history(st.session_state['messages'], st.session_state.session_key, st.session_state['model'])
            



def get_summary(session_messages, model):
    print("Saving....")
    conversation_string = "\n".join(
        f"{message['role']}: {message['content']}" for message in session_messages
    )
    word_limit = max(10, len(conversation_string) // 4)

    fpc = ['Knowly', 'I', 'Me', 'My', 'Mine', 'Myself']
    spc = ['You', 'Your', 'Yours', 'Yourself', 'Yourselves']

    prompt = f"""**In the following conversation,**

    Rewrite the summary but this time replace any references to Assistant or system with first person perspective (Helping first person pronouns: {fpc}). And replace any references to the user in second person perspective.

    {conversation_string}
"""
    
    prompt_1 = f"""
    Summarize this conversation in a single paragraph, ensuring the summary is within {word_limit} words.

    Start with "Sure here is the conversation summary."
    {prompt}
"""
    
    llama_prompt = f"""
<s>[INST] <<SYS>>
Summarize the following conversation in a single paragraph within {word_limit} words, starting with "Here is a summary of the conversation:"
<</SYS>>

{conversation_string} [/INST]
"""
    llama_prompt_2 = f"""
<s>[INST] <<SYS>>
**In the following conversation,**
Rewrite the summary but this time replace any references to Assistant or system with first person perspective (Helping first person pronouns: {fpc}). And replace any references to the user in second person perspective.
<</SYS>>

{llama_prompt} [/INST]
"""
    if "gemma" in model:
        response = ollama.chat(model=model, messages=[
            {'role': 'system', 'content': prompt_1},
            {'role': 'user', 'content': conversation_string},
        ])
    else:
        response = ollama.chat(model=model, messages=[
            {'role': 'system', 'content': llama_prompt},
            {'role': 'user', 'content': conversation_string},
        ])

    session_messages.append({"role": "assistant", "content": response})
    
    return session_messages