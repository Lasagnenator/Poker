import json

file_path = "./database.json"

table = dict()

def load_table():
    global table
    with open(file_path, "r") as f:
        table = json.load(f)

def save_table():
    with open(file_path, "w") as f:
        json.dump(table, f)

def retrieve(username, password):
    try:
        return table[username+password]
    except KeyError:
        return 5000

def set_val(username, password, value):
    table[username+password] = value
    save_table()
