import json
from datetime import datetime

def save_chat_history(chat_history,session_key):
    file_name = "sessions/" + session_key
    with open(file_name, "w") as f:
        json.dump(chat_history, f)

def load_chat_history_json(session_name):
    with open(f"sessions/{session_name}", "r") as f:
        json_data = json.load(f)
    return json_data
    
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")