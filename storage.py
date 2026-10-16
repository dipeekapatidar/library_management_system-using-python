"""Tiny JSON file storage: each record type lives in data/<name>.json"""
import json
import os
from config import DATA_DIR


def _path(name):
    return os.path.join(DATA_DIR, f"{name}.json")


def load(name):
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(_path(name)):
        return []
    try:
        with open(_path(name), "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save(name, rows):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(_path(name), "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
