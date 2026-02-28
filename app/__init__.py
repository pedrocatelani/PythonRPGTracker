from datetime import datetime
import json
from pathlib import Path


class App:
    file_path = "generic.json"
    standard_format = {
        "name": "nome",
        "description": "Se desejar, pode adicionar uma descrição aqui!",
        "created": datetime.now().strftime("%Y-%m-%d"),
        "modified": datetime.now().strftime("%Y-%m-%d"),
        "level": 1,
        "bonuses": [],
        "powers": [],
        "attributes": {"for": 0, "des": 0, "con": 0, "int": 0, "car": 0, "sab": 0},
        "status": {
            "pv": 0,
            "pvt": 0,
            "current_pv": 0,
            "pm": 0,
            "pmt": 0,
            "current_pm": 0,
            "attack": 0,
            "defense": 0,
            "damage": 0,
            "damage_reduction": 0,
            "atk_atr": "",
        },
    }

    def __init__(self, file: str):
        if file:
            self.file_path = file
        self.load_file()

    def load_file(self):
        path = Path(self.file_path)

        if not path.exists():
            # if file does not yet exists, create it and return standard format
            obj = self.standard_format

            with open(path, "w", encoding="utf-8") as f:
                json.dump(obj, f, indent=4, ensure_ascii=False)

            return obj

        else:
            # if file exists, return it
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
