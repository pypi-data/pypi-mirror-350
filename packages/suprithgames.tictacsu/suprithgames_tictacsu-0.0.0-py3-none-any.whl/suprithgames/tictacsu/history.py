# tictacsu/history.py

import os

HISTORY_FILE = "game_history.txt"

def save_result(player_name, result):
    with open(HISTORY_FILE, "a") as file:
        file.write(f"{player_name} - {result}\n")

def get_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as file:
        return file.readlines()

def clear_history():
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
