from functools import wraps
from flask import request , current_app ,redirect , url_for,abort,jsonify
from flask_login import current_user
from ..func import *

EXEMPT_METHODS=['POST','GET']

def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.is_authenticated:
            return func(*args, **kwargs)
        else:
            return current_app.login_manager.unauthorized()
    return decorated_view


