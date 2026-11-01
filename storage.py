import json
import os


def storage():
    file_path = os.path.join(os.path.dirname(__file__), "activities.json")

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    return data
