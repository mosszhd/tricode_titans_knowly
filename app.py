import streamlit as st
from llm_chains import load_normal_chain
from langchain.memory import StreamlitChatMessageHistory
from streamlit_mic_recorder import mic_recorder
from langchain_community.llms import CTransformers
from langchain.llms.ollama import Ollama
import yaml
from audio_handler import transcribe_audio


with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

def load_chain(chat_history, model, selected_model):
    return load_normal_chain(chat_history, model, selected_model)

def clear_input_field():
    st.session_state.user_question = st.session_state.user_input
    st.session_state.user_input = ""

def set_send_input():
    st.session_state.send_input = True 
    clear_input_field()

def load_model(option):
    if option == "TinyLlama":
        llm = Ollama(model=config[option]["model_name"],
                     temperature=config[option]["temperature"])
        
    elif option == "Llama2" or option == "Mistral":
        model_path = config[option]['model_path']['large']
        model_type = config[option]["model_type"]
        model_config = config[option]["model_config"]
        llm = CTransformers(model=model_path, model_type=model_type, config=model_config)
    return llm

def main():
    model_container = st.container()

    # model selecting starts
    with model_container:
        option = st.selectbox("Select a model:", 
                              ('TinyLlama', 'Llama2', 'Mistral'), 
                              index = 0, 
                              key="selected_model")
        if "model_option" not in st.session_state or st.session_state.model_option != option:
            st.session_state.model_option = option
            if "loaded_model" in st.session_state:
                del st.session_state.loaded_model
            st.session_state.loaded_model = load_model(st.session_state.model_option)

        st.write('You selected:', option)
    # model selection ends

    st.title("Knowly")
    chat_history = StreamlitChatMessageHistory(key="history")
    llm_chain = load_chain(chat_history, st.session_state.loaded_model, option)

    # input container
    input_container = st.container()
    with input_container:
        chat_input_column, voice_recording_column = st.columns([0.82, 0.18], gap="small")
        with chat_input_column:  # taking text input
            prompt = st.chat_input("What is up?")
        with voice_recording_column:  # taking voice input
            voice_recording = mic_recorder(start_prompt="Start recording", stop_prompt="Stop recording", just_once=True)
    
    # if user input is voice
    if voice_recording:
        transcribed_audio_prompt = transcribe_audio(voice_recording["bytes"])
        llm_response = llm_chain.run(transcribed_audio_prompt)
    
    # if user input is text
    if prompt:
        llm_response = llm_chain.run(prompt)

    # chat history container
    chat_history_container = st.container()
    with chat_history_container:
        if chat_history.messages != []:
            reversed_history = list(reversed(chat_history.messages))
            history_length = len(reversed_history)
            for i in range(0, history_length, 2):
                with st.chat_message(reversed_history[i+1].type):
                    st.markdown(reversed_history[i+1].content)
                with st.chat_message(reversed_history[i].type):
                    st.markdown(reversed_history[i].content)
        

if __name__ == "__main__":
    main()