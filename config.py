from os import urandom;

CSRF_ENABLED = True
SECRET_KEY = '00000000000000000000000000000000'

SUPPORTED_LANGUAGES = {'ua': 'Українська', 'ru': 'Русский'}
DEFAULT_LANGUAGE = 'ua'

# Логин и пароль админа для наполнения сайта
ADMIN_LOGIN = 'ADMIN_LOGIN'
ADMIN_PASSWORD = 'ADMIN_PASSWORD'

# Токен и ID канала для отправки уведомлений
TELEGRAM_TOKEN = 'TELEGRAM_TOKEN'
TELEGRAM_CHAT_ID = 'TELEGRAM_CHAT_ID'

SQLALCHEMY_BINDS = {
    'site': 'mysql://dblogin:dbpassword@dbhost/database',
}
SQLALCHEMY_TRACK_MODIFICATIONS = False
