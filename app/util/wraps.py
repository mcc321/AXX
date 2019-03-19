from functools import wraps
from flask import request , current_app ,redirect , url_for,abort,jsonify
from flask_login import current_user
from ..func import *

EXEMPT_METHODS=['POST','GET']



def admin_require(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user._get_current_object().role_id>=3:
            return func(*args, **kwargs)
        else:
            return current_app.login_manager.unauthorized()
    return decorated_view


def super_admin_require(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user._get_current_object().role_id==4:
            return func(*args, **kwargs)
        else:
            return current_app.login_manager.unauthorized()
    return decorated_view



