from flask import Blueprint

bp = Blueprint('site', __name__, template_folder='templates')

from app.site import views