''' Writing/Modifying JSON files for flashcard app '''

import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)
    
def deck_path(name):
    return os.path.join(DATA_DIR, f"{name}.json")

def list_deck_names():
    ensure_data_dir()
    return [f[:-5] for f in os.listdir(DATA_DIR) if f.endswith(".json")]

def load_deck(name):
    ensure_data_dir()
    with open(deck_path(name), "r") as f:
        return json.load(f)
    
def save_deck(deck):
    ensure_data_dir()
    with open(deck_path(deck["name"]), "w") as f:
        json.dump(deck, f, indent=2)
        
def delete_deck(name):
    path = deck_path(name)
    if os.path.exists(path):
        os.remove(path)

def rename_deck(old_name, new_name):
    deck = load_deck(old_name)
    deck["name"] = new_name
    save_deck(deck)
    delete_deck(old_name)
            