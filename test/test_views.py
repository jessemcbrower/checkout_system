# sudo pip install nose
# cd loaners
# nosetests .

import unittest

from mock import patch
from app.views import INVENTORY, USERS, DeviceManager, UserManager


class TestDeviceManager(unittest.TestCase):

	def setUp(self):
		self.dm = DeviceManager()

	@patch("__builtin__.open")
	@patch("json.load")
	def test_read_devices(self, mock_load, mock_open):
		self.dm.read_devices()
		mock_open.assert_called_with(INVENTORY)
		assert mock_load.called

	@patch("__builtin__.open")
	@patch("json.dump")
	def test_write_devices(self, mock_dump, mock_open):
		self.dm.write_devices()
		mock_open.assert_called_with(INVENTORY, "w")
		assert mock_dump.called

class TestUserManager(unittest.TestCase):

	def setUp(self):
		self.um = UserManager()

	@patch("__builtin__.open")
	@patch("json.load")
	def test_read_users(self, mock_load, mock_open):
		self.um.read_users()
		mock_open.assert_called_with(USERS)
		assert mock_load.called

	@patch("__builtin__.open")
	@patch("json.dump")
	def test_write_users(self, mock_dump, mock_open):
		self.um.write_users()
		mock_open.assert_called_with(USERS, "w")
		assert mock_dump.called