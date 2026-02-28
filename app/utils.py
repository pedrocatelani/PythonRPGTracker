import json
import streamlit as st
import random as rd

from datetime import datetime
from pathlib import Path

from app.constants import TRAINING_MODIFIER


def get_character_files():
    chars = []
    current_dir = Path(".")

    json_files = list(current_dir.glob("*.json"))

    if json_files:
        for file in json_files:
            chars.append(file.name)

    return chars


def add_a_buff(file_path: str, name: str):
    new_buff = {
        "key": str(rd.randint(1111111111, 9999999999)),
        "name": name,
        "description": "Gasto de Mana, tempo, tipo de ação, de onde vem....",
        "value": 0,
        "target": "des",
        "is_active": True,
    }

    with open(file_path, "r", encoding="utf-8") as file:
        obj = json.load(file)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    obj["modified"] = timestamp
    obj["bonuses"].append(new_buff)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(obj, file, indent=4, ensure_ascii=False)


def delete_a_buff(file_path: str, key: str):
    with open(file_path, "r", encoding="utf-8") as file:
        obj = json.load(file)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    obj["modified"] = timestamp

    obj["bonuses"] = [buff for buff in obj["bonuses"] if buff.get("key") != key]

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(obj, file, indent=4, ensure_ascii=False)


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


def change_status(file_path: str, key: str, modifier: int):
    with open(file_path, "r") as file:
        obj = json.load(file)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    obj["modified"] = timestamp
    obj["status"][key] += modifier

    with open(file_path, "w") as file:
        json.dump(obj, file, ensure_ascii=False)


def change_buff(file_path: str, key: str, value_key: str, new_value):
    with open(file_path, "r", encoding="utf-8") as file:
        obj = json.load(file)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    obj["modified"] = timestamp

    for b in obj["bonuses"]:
        if b["key"] == key:
            b[value_key] = st.session_state[new_value]

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(obj, file, indent=4, ensure_ascii=False)


def get_train_modifier(level: int) -> int:
    l = 1 if level < 7 else 7
    l = 7 if level < 15 else 15

    return TRAINING_MODIFIER[f"{l}"]


def create_buffs_dict(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        obj = json.load(file)

    buffs = {
        "des": 0,
        "for": 0,
        "con": 0,
        "int": 0,
        "sab": 0,
        "car": 0,
        "ataque": 0,
        "defesa": 0,
        "dano": 0,
    }

    for b in obj["bonuses"]:
        if b["is_active"]:
            buffs[b["target"]] += b["value"]

    return buffs
