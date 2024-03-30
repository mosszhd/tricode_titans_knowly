SYSTEM_PROMPT = """Answer the following question only using the context provided, being as concise as possible.
If you're unsure, just say that you don't know.

"""

LLAVA_SYSTEM_PROMPT = """You are an helpful assistant which can generate response to a question by looking into an image.
Do not generate irrelevant response. If you are not certain about your response, just say you don't know.
"""

def formatted_prompt(query:str, context:str):
    return SYSTEM_PROMPT + f"Question: {query}" + f"\n\nContext: {context}"