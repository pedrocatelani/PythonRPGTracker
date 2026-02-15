import json
import streamlit as st

from datetime import datetime
from pathlib import Path


def get_character_files():
    chars = []
    current_dir = Path(".")

    json_files = list(current_dir.glob("*.json"))

    if json_files:
        for file in json_files:
            chars.append(file.name)

    return chars


def write_changes(file_path: str, key: str, new_value: str):
    if new_value in st.session_state:
        value = st.session_state[new_value]
    else:
        value = new_value

    with open(file_path, "r") as file:
        obj = json.load(file)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    obj["modified"] = timestamp
    obj[key] = value

    with open(file_path, "w") as file:
        json.dump(obj, file, ensure_ascii=False)
