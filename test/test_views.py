import unittest
from unittest.mock import patch

from app.config import INVENTORY, USERS
from app.models import UserManager, DeviceManager  # Import DeviceManager from models

class TestDeviceManager(unittest.TestCase):

    def setUp(self):
        self.dm = DeviceManager()

    @patch("builtins.open")  # Updated for Python 3
    @patch("json.load")
    def test_read_devices(self, mock_load, mock_open):
        self.dm.read_devices()
        mock_open.assert_called_with(INVENTORY)
        assert mock_load.called

    @patch("builtins.open")  # Updated for Python 3
    @patch("json.dump")
    def test_write_devices(self, mock_dump, mock_open):
        self.dm.write_devices()
        mock_open.assert_called_with(INVENTORY, "w")
        assert mock_dump.called

class TestUserManager(unittest.TestCase):

    def setUp(self):
        self.um = UserManager()

    @patch("builtins.open")  # Updated for Python 3
    @patch("json.load")
    def test_read_users(self, mock_load, mock_open):
        self.um.read_users()
        mock_open.assert_called_with(USERS)
        assert mock_load.called

    @patch("builtins.open")  # Updated for Python 3
    @patch("json.dump")
    def test_write_users(self, mock_dump, mock_open):
        self.um.write_users()
        mock_open.assert_called_with(USERS, "w")
        assert mock_dump.called
