import ollama
import json

def get_gemma_summary(session_messages, model):

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
    print("\n\ngenerating response...")
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

    summary = response["message"]["content"]

    return summary

def get_summary(session_messages, model):

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
    print("\n\ngenerating response...")
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
    print("\n\n")
    print(response)
    print("\n\n")
    
    
    return summary


filename = './sessions/2024-03-30-09-50-00.json'
print("\n\n")
with open(filename,"r",encoding='utf-8') as f:
    try:
      # Read the entire file content
      data = f.read()
      # Check for potential hidden characters at the beginning/end (optional)
      data = data.strip()
      session_messages = json.loads(data)
    except json.decoder.JSONDecodeError as e:
      print(f"Error decoding JSON: {e}")
summary = get_summary(session_messages=session_messages,model='tinyllama')
print(summary)