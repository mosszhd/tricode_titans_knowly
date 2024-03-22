import streamlit as st
from langchain.memory import StreamlitChatMessageHistory
from langchain_community.llms import CTransformers
from langchain.llms.ollama import Ollama
import yaml

from llm_chains import newChatChain
from langchain_core.messages import HumanMessage, AIMessage


with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)


def clear_input_field():
    st.session_state.user_question = st.session_state.user_input
    st.session_state.user_input = ""

def set_send_input():
    st.session_state.send_input = True 
    clear_input_field()

def load_model(option):
    if option == "TinyLlama":
        llm = Ollama(model=config[option]["model_name"],
                     temperature=config[option]["temperature"],
                     stop=config[option]["stop_tokens"])
        
    elif option == "Llama2" or option == "Mistral":
        model_path = config[option]['model_path']['large']
        model_type = config[option]["model_type"]
        model_config = config[option]["model_config"]
        llm = CTransformers(model=model_path, model_type=model_type, config=model_config)
    return llm


# function for generating stream generator
def get_response(query, chat_history, selected_model):
    llm = st.session_state.loaded_model
    chain = newChatChain(llm=llm, selected_model=selected_model, chat_history=chat_history)
    return chain.run(query, chat_history)


def main():
    model_container = st.container()

    with model_container:
        option = st.selectbox("Select a model:", 
                              ("TinyLlama", 'Llama2', 'Mistral'), 
                              index = 0, 
                              key="selected_model")
        if "model_option" not in st.session_state or st.session_state.model_option != option:
            st.session_state.model_option = option
            st.session_state.loaded_model = load_model(st.session_state.model_option)

        st.write('You selected:', option)

    st.title("Knowly")

    # creating chat history once
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = StreamlitChatMessageHistory(key="history")


    # loading previous conversation if there is any
    if st.session_state.chat_history.messages != []:
        for message in st.session_state.chat_history.messages:
            if isinstance(message, HumanMessage):
                with st.chat_message("user"):
                    st.markdown(message.content)
            elif isinstance(message, AIMessage):
                with st.chat_message("assistant"):
                    st.markdown(message.content)

    prompt = st.chat_input("What is up?")

    # passing prompt to the llm chain and saving the conversation
    if prompt:
        st.session_state.chat_history.messages.append(HumanMessage(prompt))
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            ai_response = st.write_stream(get_response(query=prompt, chat_history=st.session_state.chat_history, selected_model=option))
        st.session_state.chat_history.messages.append(AIMessage(ai_response))


# main call
if __name__ == "__main__":
    main()