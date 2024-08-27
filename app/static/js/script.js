// app/static/js/script.js

function editUser(username) {
    document.getElementById('username-display-' + username).style.display = 'none';
    document.getElementById('role-display-' + username).style.display = 'none';
    document.getElementById('username-input-' + username).style.display = 'block';
    document.getElementById('role-input-' + username).style.display = 'inline-block';
    document.getElementById('role-label-' + username).style.display = 'inline-block';
    document.getElementById('save-button-' + username).style.display = 'inline-block';
    document.getElementById('cancel-button-' + username).style.display = 'inline-block';
    document.getElementById('edit-button-' + username).style.display = 'none';
}

function cancelEdit(username) {
    document.getElementById('username-display-' + username).style.display = 'block';
    document.getElementById('role-display-' + username).style.display = 'block';
    document.getElementById('username-input-' + username).style.display = 'none';
    document.getElementById('role-input-' + username).style.display = 'none';
    document.getElementById('role-label-' + username).style.display = 'none';
    document.getElementById('edit-button-' + username).style.display = 'inline-block';
    document.getElementById('save-button-' + username).style.display = 'none';
    document.getElementById('cancel-button-' + username).style.display = 'none';
}

function showInputsBeforeSubmit(username) {
    document.getElementById('username-input-' + username).style.display = 'block';
    document.getElementById('role-input-' + username).style.display = 'inline-block';
}

function editDevice(deviceId) {
    document.getElementById('device-name-display-' + deviceId).style.display = 'none';
    document.getElementById('device-type-display-' + deviceId).style.display = 'none';
    document.getElementById('asset-tag-display-' + deviceId).style.display = 'none';
    document.getElementById('checked-out-display-' + deviceId).style.display = 'none';
    document.getElementById('device-name-input-' + deviceId).style.display = 'block';
    document.getElementById('device-type-input-' + deviceId).style.display = 'block';
    document.getElementById('asset-tag-input-' + deviceId).style.display = 'block';
    document.getElementById('checked-out-input-' + deviceId).style.display = 'block';
    document.getElementById('save-button-' + deviceId).style.display = 'inline-block';
    document.getElementById('cancel-button-' + deviceId).style.display = 'inline-block';
    document.getElementById('edit-button-' + deviceId).style.display = 'none';
}

function cancelDeviceEdit(deviceId) {
    document.getElementById('device-name-display-' + deviceId).style.display = 'block';
    document.getElementById('device-type-display-' + deviceId).style.display = 'block';
    document.getElementById('asset-tag-display-' + deviceId).style.display = 'block';
    document.getElementById('checked-out-display-' + deviceId).style.display = 'block';
    document.getElementById('device-name-input-' + deviceId).style.display = 'none';
    document.getElementById('device-type-input-' + deviceId).style.display = 'none';
    document.getElementById('asset-tag-input-' + deviceId).style.display = 'none';
    document.getElementById('checked-out-input-' + deviceId).style.display = 'none';
    document.getElementById('edit-button-' + deviceId).style.display = 'inline-block';
    document.getElementById('save-button-' + deviceId).style.display = 'none';
    document.getElementById('cancel-button-' + deviceId).style.display = 'none';
}

function showDeviceInputsBeforeSubmit(deviceId) {
    document.getElementById('device-name-input-' + deviceId).style.display = 'block';
    document.getElementById('device-type-input-' + deviceId).style.display = 'block';
    document.getElementById('asset-tag-input-' + deviceId).style.display = 'block';
    document.getElementById('checked-out-input-' + deviceId).style.display = 'block';
}
