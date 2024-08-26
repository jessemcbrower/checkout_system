class Config:
    SECRET_KEY = 'you-will-never-guess'
    WTF_CSRF_ENABLED = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'mcbrower.checkoutsystem@gmail.com'
    MAIL_PASSWORD = 'Checkmate'

    INVENTORY = 'app/devices.json'
    USERS = 'app/users.json'
