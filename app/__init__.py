from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'admin.login'

from app.admin import bp as admin
app.register_blueprint(admin, url_prefix='/admin')

from app.site import bp as site
app.register_blueprint(site, url_prefix='/<lang>')

#from app.cabinet import bp as cabinet
#app.register_blueprint(cabinet, url_prefix='/cabinet')
