from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config
from app.models import DeviceManager, UserManager

# Initialize the Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Initialize Flask-Mail
mail = Mail(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'index'  # Redirect to 'index' if user is not logged in
login_manager.init_app(app)

# Initialize DeviceManager and UserManager
device_manager = DeviceManager()
user_manager = UserManager()

# Import routes after initializing extensions to avoid circular imports
from app import routes
