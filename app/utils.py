import json

def load_json(file_path):
    with open(file_path) as file:
        return json.load(file)

def write_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file)
