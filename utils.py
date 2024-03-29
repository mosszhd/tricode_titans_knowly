import json
from datetime import datetime
import ollama



def save_chat_history(chat_history,session_key):
    print(chat_history)
    file_name = f"sessions/{session_key}"
    with open(file_name, "w") as f:
        json.dump(chat_history, f)

def load_chat_history_json(session_name):
    filename = f"sessions/{session_name}"
    with open(filename, "r") as f:
        json_data = json.load(f)
    return json_data
    
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

def get_summary(session_messages):

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

    response = ollama.chat(model='gemma:2b', messages=[
        {'role': 'system', 'content': prompt_1},
        {'role': 'user', 'content': conversation_string},
    ])

    summary = response["message"]["content"]
    
    return summary