from flask import render_template, abort, redirect, flash, request, get_flashed_messages
from flask_login import login_required, login_user, logout_user, current_user
from app import app, device_manager, user_manager, login_manager
from .forms import DeviceInfo, LoginForm
from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return user_manager.get_user(user_id)

def generate_device_id():
    if device_manager.devices:
        max_id = max(device['id'] for device in device_manager.devices)
        return max_id + 1
    return 1

@app.route('/', methods=['GET'])
def index():
    form = LoginForm()
    return render_template('index.html', form=form)

@app.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    get_flashed_messages()  # Clears any existing messages
    username = form.username.data
    password = form.password.data

    for user in user_manager.users:
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
    get_flashed_messages()  # Clears any existing messages
    logout_user()
    flash('You have been logged out.')
    return redirect('/')

@app.route('/devices')
@login_required
def devices():
    devices = device_manager.devices
    return render_template('devices.html', devices=devices)

@app.route('/devices/add', methods=['GET', 'POST'])
@login_required
def add_device():
    form = DeviceInfo()
    if form.validate_on_submit():
        device_name = form.name.data
        device_type = form.type.data
        device_tag = form.tag.data
        
        if device_name and device_type and device_tag:
            new_device = {
                'name': device_name,
                'type': device_type,
                'user': 'Available',  # Automatically set as available
                'tag': device_tag,
                'id': generate_device_id()
            }
            device_manager.devices.append(new_device)
            device_manager.write_devices()
            return redirect('/devices')
    return render_template('add.html', form=form)

@app.route('/devices/<int:device_id>', methods=['GET', 'POST'])
@login_required
def device(device_id):
    device = device_manager.get_device(device_id)
    
    if request.method == 'GET':
        if not device:
            abort(404)
        return render_template('device.html', device=device)
    
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'checkin':
            updated_device = device_manager.add_or_update_device(device_id)
        elif action == 'checkout':
            updated_device = device_manager.add_or_update_device(device_id, str(current_user.id))
        else:
            abort(400)  # Invalid action
        if not updated_device:
            abort(404)
        return redirect('/devices')

@app.route('/devices/<int:device_id>/delete', methods=['POST'])
@login_required
def delete_device(device_id):
    device = device_manager.get_device(device_id)
    if device:
        device_manager.delete_device(device_id)
        flash(f"Device {device['name']} deleted successfully.")
    else:
        flash("Device not found.")
    return redirect('/devices')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            # Check if the username already exists
            for user in user_manager.users:
                if user['username'] == username:
                    flash('Username already exists')
                    return redirect('/register')

            # Add the new user
            new_user = {'username': username, 'password': password}
            user_manager.users.append(new_user)
            user_manager.write_users()
            flash('User registered successfully!')
            return redirect('/')
    return render_template('register.html', form=form)

@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user_id = current_user.id
    
    # Find and remove the user from the user manager
    user_manager.users = [user for user in user_manager.users if user['username'] != user_id]
    user_manager.write_users()
    
    # Clear old flash messages
    get_flashed_messages()

    # Log the user out and redirect to the home page
    logout_user()
    flash('Your account has been deleted.')
    return redirect('/')
