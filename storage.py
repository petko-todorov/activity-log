import json
import os

file_path = os.path.join(os.path.dirname(__file__), "activities.json")


def storage():
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    return data


def save(data):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
