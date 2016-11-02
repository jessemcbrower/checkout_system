from flask import render_template, jsonify, abort, make_response, request, redirect, Response, flash
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_mail import Mail, Message
from app import app
from .forms import DeviceInfo, LoginForm
import json
import hashlib

INVENTORY = 'app/devices.json'
USERS = 'app/users.json'


class DeviceManager():

    def __init__(self):
        self.devices = None

    def read_devices(self):
        with open(INVENTORY) as devices:
            self.devices = json.load(devices)

    def write_devices(self):
        with open(INVENTORY, 'w') as outfile:
            json.dump(self.devices, outfile)

dm = DeviceManager()
dm.read_devices()

class User(UserMixin):
    pass

class UserManager():

    def __init__(self):
        self.users = None

    def read_users(self):
        with open(USERS) as users:
            self.users = json.load(users)

    def write_users(self):
        with open(USERS, 'w') as outfile:
            json.dump(self.users, outfile)

um = UserManager()
um.read_users()

login_manager = LoginManager()
login_manager.init_app(app)

mail = Mail()
mail.init_app(app)

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('unauthorized.html')

@app.route('/')
def index():
    form = LoginForm()
    return render_template('index.html', form=form, devices=dm.devices)

@app.route('/register', methods=['GET', 'POST'])
def add_user():
    if request.method == 'GET':
        form = LoginForm()
        return render_template('register.html', form=form)
    elif request.method == 'POST':
        # password = request.form.get('password')
        user = {
            # 'firstname': request.form.get('firstname'),
            # 'lastname': request.form.get('lastname'),
            # 'email': request.form.get('lastname'),
            'username': request.form.get('username'),
            'password': request.form.get('password')
            # 'password': hashlib.sha1(password)
        }
        if request.form.get('password') != request.form.get('confirm'):
            flash('Passwords must match.')
            return redirect('/register')
        flash(user['username'] + ' was created successfully')
        um.users.append(user)
        um.write_users()
        return redirect('/')

@login_manager.user_loader
def user_loader(username):
    um.read_users()
    for user in um.users:
        if username == user['username']:
            user = User()
            user.id = username
            return user


@login_manager.request_loader
def request_loader(request):
    um.read_users()
    username = request.form.get('username')
    password = request.form.get('password')
    for user in um.users:
        if user['username'] == username and user['password'] == password:
            user = User()
            user.id = username
            user.is_authenticated = True
            return user

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    for user in um.users:
        if request.form['username'] == user['username'] and request.form['password'] == user['password']:
            user = User()
            user.id = username
            login_user(user)
            return redirect('/devices')

    return render_template('badlogin.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/devices', methods=['GET'])
@login_required
def get_devices():
    return render_template('devices.html', devices=dm.devices, user=um.users)

@app.route('/devices/add', methods=['GET', 'POST'])
def add_device():
    if request.method == 'GET':
        form = DeviceInfo()
        return render_template('add.html', form=form)
    elif request.method == 'POST':
        if len(dm.devices) == 0:
            id = 1
        else:
            id = dm.devices[-1]['id'] + 1
        device = {
            'id': id,
            'name': "Loaner-" + str(id),
            'type': request.form.get('type'),
            'user': "Available",
            'tag': request.form.get('tag')
        }
        dm.devices.append(device)
        dm.write_devices()
        return redirect('/devices')

@app.route('/devices/<int:device_id>', methods=['GET', 'POST', 'DELETE'])
def get_device(device_id):
    if request.method == 'GET':
        form = DeviceInfo()
        device = match_device(device_id)
        if len(device) == 0:
            return redirect('/devices')
        return render_template('device.html', device=device[0], form=form)

    elif request.method == 'POST':
        device = match_device(device_id)
        # NEED TO CREATE NEW GMAIL ACCOUNT BEFORE THIS FEATURE WILL WORK AGAIN
        msg = Message(device[0]['name'] + " has been reserved by " + str(current_user.id),
                        sender="globe.loaners@gmail.com",
                        recipients=["globe.loaners@gmail.com"])
        if len(device) == 0:
            return redirect('/devices')
        elif device[0]['user'] == 'Available':
            device[0]['user'] = str(current_user.id)
            # NEED TO CREATE NEW GMAIL ACCOUNT BEFORE THIS FEATURE WILL WORK AGAIN
            mail.send(msg)
        else:
            device[0]['user'] = 'Available'
        dm.write_devices()
        return redirect('/devices')
        
    elif request.method == 'DELETE':
        device = match_device(device_id)
        if len(device) == 0:
            abort(404)
        dm.devices.remove(device[0])
        dm.write_devices()
        return 'OK'

def match_device(device_id):
    return [device for device in dm.devices if device['id'] == device_id]

@app.errorhandler(400)
def device_exists(error):
    return make_response(jsonify({'error': 'Device name already exists; please choose another'}))

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
