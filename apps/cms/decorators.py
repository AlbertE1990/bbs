from functools import wraps
from flask import session,redirect,url_for
import config

def login_required(func):

    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get(config.CMS_USER_ID):
            return func(*args,**kwargs)
        else:
            return redirect(url_for("cms.login"))
    return wrapper

