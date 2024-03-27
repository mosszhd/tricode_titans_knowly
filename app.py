import streamlit as st
from llm_chains import load_normal_chain
from langchain.memory import StreamlitChatMessageHistory
from langchain_community.llms import CTransformers
from langchain.llms.ollama import Ollama
from rag_chain import create_or_load_vectorstore, get_compressed_retriever, ragChain
import yaml
import os

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

    st.title("Knowly")

    # pdf upload
    uploaded_docs = st.sidebar.file_uploader(label="Upload pdf or text files", accept_multiple_files=True, key="document_uploader", type=["pdf"])

    if uploaded_docs and "compressed_retriever" not in st.session_state.keys():
        print("uploaded docs section is running...")
        with st.spinner("Processing documents..."):
            # saving the uploaded files in directory
            save_dir = config["documents_path"]
            for file_item in uploaded_docs:
                with open(f"{save_dir}/{file_item.name}", "wb") as f:
                    f.write(file_item.getbuffer())
                f.close()
        
        if len(os.listdir(config["documents_path"])) != 0:
            vector_db = create_or_load_vectorstore()  # creating vector database
            st.session_state.compressed_retriever = get_compressed_retriever(llm=st.session_state.loaded_model, vector_db=vector_db, k=1)
    elif "vectorstore" in os.listdir(os.getcwd()):
        loaded_vector_db = create_or_load_vectorstore(load=True)
        st.session_state.compressed_retriever = get_compressed_retriever(llm=st.session_state.loaded_model, vector_db=loaded_vector_db, k=1)

    chat_history = StreamlitChatMessageHistory(key="history")

    # pdf chat
    pdf_chat_mode = st.sidebar.toggle(label="PDF Chat", key="pdf_chat", value=False, disabled=True if "compressed_retriever" not in st.session_state.keys() else False)

    if pdf_chat_mode:
        if "compressed_retriever" not in st.session_state.keys():
            vector_db = create_or_load_vectorstore(load=True)  # loading vector database
            st.session_state.compressed_retriever = get_compressed_retriever(llm=st.session_state.loaded_model, vector_db=vector_db, k=1)
        llm_chain = ragChain(llm=st.session_state.loaded_model, chat_history=chat_history, retriever=st.session_state.compressed_retriever)
        print("PDF chat is enabled...")
    else:
        llm_chain = load_chain(chat_history, st.session_state.loaded_model, option)
        print("Chat with normal chain...")

    if chat_history.messages != []:
        for message in chat_history.messages:
            with st.chat_message(message.type):
                st.markdown(message.content)

    prompt = st.chat_input("What is up?")

    if prompt:
        if pdf_chat_mode:
            with st.chat_message("user"):
                chat_history.add_user_message(prompt)
                st.markdown(prompt)
                pdf_llm_response = llm_chain.run(query=prompt)
            with st.chat_message("assistant"):
                chat_history.add_ai_message(pdf_llm_response)
                st.markdown(pdf_llm_response)
        else:
            with st.chat_message("user"):
                st.markdown(prompt)
                llm_response = llm_chain.run(prompt)
            with st.chat_message("assistant"):
                st.markdown(llm_response)

if __name__ == "__main__":
    main()