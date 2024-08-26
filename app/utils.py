import json
from app.config import INVENTORY, USERS  # Updated import

def load_json(file_path):
    with open(file_path) as file:
        return json.load(file)

def write_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file)

def match_device(device_id, devices):
    return [device for device in devices if device['id'] == device_id]
