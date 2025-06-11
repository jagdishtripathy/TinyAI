import json
import pandas as pd
from config import PROFILE_PATH, MEMORY_PATH, CHAT_HISTORY_PATH, MYDATA_CSV, LOG_PATTERNS_CSV

def load_json(path, default):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return default

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f)

def load_data():
    user_profile = load_json(PROFILE_PATH, {"interests": []})
    memory_facts = load_json(MEMORY_PATH, [])
    chat_history = load_json(CHAT_HISTORY_PATH, [])
    df = pd.read_csv(MYDATA_CSV)
    log_df = pd.read_csv(LOG_PATTERNS_CSV)
    return user_profile, memory_facts, chat_history, df, log_df