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
            json.dump(self.devices, file)

    def get_device(self, device_id):
        for device in self.devices:
            if device['id'] == device_id:
                return device
        return None

    def add_or_update_device(self, device_id, user_id=None):
        device = self.get_device(device_id)
        if device:
            if user_id:  # If a user is provided, check out the device
                device['user'] = user_id
            else:  # Otherwise, check in the device
                device['user'] = 'Available'
            self.write_devices()
            return device
        return None

    def delete_device(self, device_id):
        device = self.get_device(device_id)
        if device:
            self.devices.remove(device)
            self.write_devices()
            return device
        return None

class User(UserMixin):
    def __init__(self, username):
        self.id = username

class UserManager:
    def __init__(self):
        self.users = self.read_users()

    def read_users(self):
        with open(Config.USERS) as file:
            return json.load(file)

    def write_users(self):
        with open(Config.USERS, 'w') as file:
            json.dump(self.users, file)

    def get_user(self, user_id):
        for user in self.users:
            if user['username'] == user_id:
                return User(user['username'])
        return None
