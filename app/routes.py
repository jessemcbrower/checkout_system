from flask import render_template, abort, redirect, flash, request, get_flashed_messages, url_for
from flask_login import login_required, login_user, logout_user, current_user
from app import app, device_manager, user_manager, login_manager
from .forms import DeviceInfo, LoginForm, RegistrationForm
from app.models import User
from functools import wraps
import random
import string

@login_manager.user_loader
def load_user(user_id):
    return user_manager.get_user(user_id)

def generate_device_id():
    if device_manager.devices:
        max_id = max(device['id'] for device in device_manager.devices)
        return max_id + 1
    return 1

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/', methods=['GET'])
def index():
    form = LoginForm()
    return render_template('index.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        for user in user_manager.users:
            if user['username'] == username and user['password'] == password:
                user_obj = User(username, user.get('role', 'user'))
                login_user(user_obj)
                flash('Login successful!', 'success')
                
                if user_obj.role == 'admin':
                    return redirect('/admin')
                
                return redirect('/devices')

        flash('Invalid username or password', 'danger')

    return render_template('index.html', form=form)

@app.route('/logout')
@login_required
def logout():
    get_flashed_messages()
    logout_user()
    flash('You have been logged out.')
    return redirect('/')

@app.route('/devices')
@login_required
def devices():
    devices = device_manager.devices
    return render_template('devices.html', devices=devices)

@app.route('/admin/add_device', methods=['GET', 'POST'])
@login_required
@admin_required
def add_device():
    form = DeviceInfo()  # Assuming DeviceInfo is your Flask-WTF form class
    
    if form.validate_on_submit():
        new_device = {
            'id': generate_device_id(),
            'name': form.name.data,
            'type': form.type.data,
            'tag': form.tag.data,
            'user': 'Available'
        }
        device_manager.devices.append(new_device)
        device_manager.write_devices()

        flash('Device added successfully.', 'success')
        return redirect(url_for('admin_panel'))

    # Render the form if it’s a GET request
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
            abort(400)
        if not updated_device:
            abort(404)
        return redirect('/devices')

@app.route('/admin/delete_device/<int:device_id>', methods=['POST'])
@login_required
@admin_required
def delete_device(device_id):
    device_manager.devices = [device for device in device_manager.devices if device['id'] != device_id]
    device_manager.write_devices()
    flash('Device deleted successfully.', 'success')
    return redirect(url_for('admin_panel'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            # Assign a default role if none is provided
            role = 'user'

            for user in user_manager.users:
                if user['username'] == username:
                    flash('Username already exists', 'danger')
                    return render_template('register.html', form=form)

            new_user = {'username': username, 'password': password, 'role': role}
            user_manager.users.append(new_user)
            user_manager.write_users()

            flash('User registered successfully!', 'success')

            if current_user.is_authenticated and current_user.role == 'admin':
                return redirect(url_for('admin_panel'))
            else:
                return redirect('/login')

        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", 'danger')
    
    return render_template('register.html', form=form)

@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user_id = current_user.id
    
    user_manager.users = [user for user in user_manager.users if user['username'] != user_id]
    user_manager.write_users()
    
    get_flashed_messages()

    logout_user()
    flash('Your account has been deleted.')
    return redirect('/')

@app.route('/admin')
@login_required
@admin_required
def admin_panel():
    users = user_manager.users
    devices = device_manager.devices  # Ensure devices are fetched here
    return render_template('admin_panel.html', users=users, devices=devices)

@app.route('/admin/reset_password/<username>', methods=['POST'])
@login_required
@admin_required
def reset_password(username):
    new_password = generate_random_password()

    for user in user_manager.users:
        if user['username'] == username:
            user['password'] = new_password
            user_manager.write_users()
            flash(f'Password reset for {username}. New password: {new_password}', 'success')
            break
    else:
        flash(f'User {username} not found.', 'danger')

    return redirect(url_for('admin_panel'))

@app.route('/admin/update_user/<username>', methods=['POST'])
@login_required
@admin_required
def update_user(username):
    print("Received form data:", request.form)  # Print all form data for debugging

    original_username = request.form.get('original_username')
    new_username = request.form.get('username')
    role_value = request.form.get('role')

    # Set role to 'user' if the checkbox is not checked, otherwise 'admin'
    role = 'admin' if role_value == 'admin' else 'user'

    print(f"Form Data Received: Original Username: {original_username}, New Username: {new_username}, Role: {role}")

    if not new_username:
        flash('Invalid username. The username cannot be empty.', 'danger')
        return redirect(url_for('admin_panel'))

    # Find and update the user
    user_updated = False
    for user in user_manager.users:
        if user['username'] == original_username:
            user['username'] = new_username
            user['role'] = role
            user_manager.write_users()  # Save changes to persistent storage
            user_updated = True
            flash(f'User {new_username} updated successfully.', 'success')
            break

    if not user_updated:
        flash(f'User {original_username} not found.', 'danger')

    return redirect(url_for('admin_panel'))

@app.route('/admin/delete_user/<username>', methods=['POST'])
@login_required
@admin_required
def delete_user(username):
    user_manager.users = [user for user in user_manager.users if user['username'] != username]
    user_manager.write_users()
    flash(f'User {username} deleted successfully.', 'success')
    return redirect(url_for('admin_panel'))

@app.route('/admin/promote_to_admin/<username>', methods=['POST'])
@login_required
@admin_required
def promote_to_admin(username):
    for user in user_manager.users:
        if user['username'] == username:
            user['role'] = 'admin'
            user_manager.write_users()
            flash(f'User {username} has been promoted to admin.', 'success')
            break
    return redirect(url_for('admin_panel'))

@app.route('/admin/demote_to_user/<username>', methods=['POST'])
@login_required
@admin_required
def demote_to_user(username):
    for user in user_manager.users:
        if user['username'] == username:
            user['role'] = 'user'
            user_manager.write_users()
            flash(f'User {username} has been demoted to user.', 'success')
            break
    return redirect(url_for('admin_panel'))

@app.route('/admin/update_device/<int:device_id>', methods=['POST'])
@login_required
@admin_required
def update_device(device_id):
    # Implement the logic to update the device here
    device_name = request.form.get('device_name')
    device_type = request.form.get('device_type')
    asset_tag = request.form.get('asset_tag')
    checked_out_to = request.form.get('checked_out_to')

    # Find and update the device
    for device in device_manager.devices:
        if device['id'] == device_id:
            device['name'] = device_name
            device['type'] = device_type
            device['tag'] = asset_tag
            device['user'] = checked_out_to
            device_manager.write_devices()
            flash(f'Device {device_name} updated successfully.', 'success')
            break
    else:
        flash(f'Device not found.', 'danger')

    return redirect(url_for('admin_panel'))
