templates = {
    "Mistral": """<s>[INST] You are an AI chatbot having a conversation with a human. Answer his questions.[/INST]
    Previous conversation: {history}
    Human: {human_input}
    AI:""",
    "Llama2": """Use the following pieces of information to answer the user's question. 
    If you don't know the answer, please just say that you don't know the answer,
    don't try to make up an answer.

    Previous conversation: {history}
    Human: {human_input}

    Only returns the helpful answer below and nothing else.
    Helpful answer:
    """
}
