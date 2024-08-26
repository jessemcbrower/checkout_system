from flask import render_template, jsonify, abort, redirect, flash, request, get_flashed_messages
from flask_login import login_required, login_user, logout_user, current_user
from app import app
from .forms import DeviceInfo, LoginForm
from app.utils import load_json, write_json, match_device
from app.config import INVENTORY, USERS
from app.models import User, um, mail  # Import from models

@app.route('/')
def index():
    form = LoginForm()
    return render_template('index.html', form=form)

@app.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    username = form.username.data
    password = form.password.data

    users = um.users  # Use UserManager instance
    for user in users:
        if user['username'] == username and user['password'] == password:
            user_obj = User(username)
            login_user(user_obj)
            flash('Login successful!')
            return redirect('/devices')

    flash('Invalid username or password')
    return redirect('/')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    get_flashed_messages()  # Clears any existing messages
    flash('You have been logged out.')
    return redirect('/')

@app.route('/devices')
@login_required
def devices():
    devices = load_json(INVENTORY)
    return render_template('devices.html', devices=devices)

@app.route('/devices/<int:device_id>', methods=['GET', 'POST', 'DELETE'])
@login_required
def device(device_id):
    devices = load_json(INVENTORY)
    device = match_device(device_id, devices)
    
    if request.method == 'GET':
        if not device:
            abort(404)
        return render_template('device.html', device=device[0])
    
    if request.method == 'POST':
        if not device:
            abort(404)
        device[0]['user'] = 'Available' if device[0]['user'] != 'Available' else str(current_user.id)
        write_json(INVENTORY, devices)
        return redirect('/devices')
        
    if request.method == 'DELETE':
        if not device:
            abort(404)
        devices.remove(device[0])
        write_json(INVENTORY, devices)
        return 'OK'
