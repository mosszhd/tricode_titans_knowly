import streamlit as st
from llm_chains import load_normal_chain
from langchain.memory import StreamlitChatMessageHistory
from langchain_community.llms import CTransformers
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

def load_chain(chat_history,model,selected_model):
    return load_normal_chain(chat_history,model,selected_model)

def clear_input_field():
    st.session_state.user_question = st.session_state.user_input
    st.session_state.user_input = ""

def set_send_input():
    st.session_state.send_input = True 
    clear_input_field()

def load_model(option):
    model_path = config[option]['model_path']['large']
    model_type = config[option]["model_type"]
    model_config = config[option]["model_config"]
    llm = CTransformers(model=model_path,model_type=model_type, config=model_config)
    return llm

def main():
    model_container = st.container()

    with model_container:
        option = st.selectbox(
        "Select a model:",
        ('Llama2', 'Mistral'),
        index = 0,
        key="selected_model")
        if "model_option" not in st.session_state or st.session_state.model_option != option:
            st.session_state.model_option = option
            st.session_state.loaded_model = load_model(st.session_state.model_option)

        st.write('You selected:', option)

    st.title("Knowly")

    chat_container = st.container()

    if "send_input" not in st.session_state:
        st.session_state.send_input = False
        st.session_state.user_question = ""

    chat_history = StreamlitChatMessageHistory(key="history")

    llm_chain = load_chain(chat_history,st.session_state.loaded_model,option)

    user_input = st.text_input("Type your message here", key="user_input", on_change=set_send_input)

    send_button = st.button("Send", key="send_button")

    if send_button or st.session_state.send_input:
        if st.session_state.user_question != "":
            with chat_container:
                llm_response = llm_chain.run(st.session_state.user_question)
                st.session_state.user_question = ""
    
    if chat_history.messages != []:
        with chat_container:
            st.write("Chat History:")
            for message in chat_history.messages:
                st.chat_message(message.type).write(message.content)

    if chat_history.messages != []:
        with chat_container:
            st.write("Chat History:")
            for message in chat_history.messages:
                st.chat_message(message.type).write(message.content)

if __name__ == "__main__":
    main()