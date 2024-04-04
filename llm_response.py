import ollama
import streamlit as st
from prompt_templates import SYSTEM_PROMPT


def formatted_prompt(query:str, context:str):
    return SYSTEM_PROMPT + f"Question: {query}" + f"\n\nContext: {context}"

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
