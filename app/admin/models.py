from app import app, lm
from flask_login import UserMixin

class Admin(UserMixin):
    id = 1
    login = app.config['ADMIN_LOGIN']
    password = app.config['ADMIN_PASSWORD']

    def check_password(self, login, pwd):
        if self.login ==login and self.password == pwd:
            return True
        else:
            return False

@lm.user_loader
def load_user(id):
    return Admin
