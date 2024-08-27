import json
from flask_login import UserMixin
from app.config import Config

class DeviceManager:
    def __init__(self):
        self.devices = self.read_devices()

    def read_devices(self):
        with open(Config.INVENTORY) as file:
            return json.load(file)

    def write_devices(self):
        with open(Config.INVENTORY, 'w') as file:
            json.dump(self.devices, file, indent=4)

    def get_device(self, device_id):
        return next((device for device in self.devices if device['id'] == device_id), None)

    def add_or_update_device(self, device_id, user_id=None):
        device = self.get_device(device_id)
        if device:
            device['user'] = user_id if user_id else 'Available'
            self.write_devices()
            return device
        return None

    def delete_device(self, device_id):
        self.devices = [device for device in self.devices if device['id'] != device_id]
        self.write_devices()

class User(UserMixin):
    def __init__(self, username, role='user'):
        self.id = username
        self.role = role

class UserManager:
    def __init__(self):
        self.users = self.read_users()

    def read_users(self):
        with open(Config.USERS) as file:
            return json.load(file)

    def write_users(self):
        print("Writing users to file...")
        with open(Config.USERS, 'w') as file:
            json.dump(self.users, file, indent=4)
        print("Users have been written successfully.")

    def get_user(self, user_id):
        user = next((user for user in self.users if user['username'] == user_id), None)
        return User(user['username'], user.get('role', 'user')) if user else None
