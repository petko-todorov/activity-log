import json
import os
import sys

if getattr(sys, "frozen", False) or "__compiled__" in globals():
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(base_dir, "activities.json")


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
