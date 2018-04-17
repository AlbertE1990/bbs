from functools import wraps
from flask import session,redirect,url_for,request,render_template
from  config import FRONT_USER_ID

def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get(FRONT_USER_ID):
            return func(*args,**kwargs)
        else:
            return redirect(url_for('front.login'))
    return wrapper

