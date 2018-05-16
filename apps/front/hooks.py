from flask import g,session,request,render_template
from .views import bp
import config
from .models import FrontUser

@bp.before_app_request
def before_request():
    user_id = session.get(config.FRONT_USER_ID)
    if user_id:
        user = FrontUser.query.get(user_id)
        if user:
            g.front_user = user

@bp.errorhandler(404)
def page_not_found(error):
    return render_template('front/front_404.html'),404