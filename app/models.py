import json
from flask_login import UserMixin, LoginManager
from flask_mail import Mail
from app import app
from app.config import USERS

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, username):
        self.id = username

# UserManager class for handling user data
class UserManager:

    def __init__(self):
        self.users = None
        self.read_users()

    def read_users(self):
        with open(USERS) as users:
            self.users = json.load(users)

    def write_users(self):
        with open(USERS, 'w') as outfile:
            json.dump(self.users, outfile)

# Instantiate the UserManager
um = UserManager()

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Initialize Flask-Mail
mail = Mail()
mail.init_app(app)
