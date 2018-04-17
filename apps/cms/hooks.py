from flask import g,session,request
from .views import bp
import config
from .models import CMSUser,CMSPermission

@bp.before_app_request
def before_request():
    user_id = session.get(config.CMS_USER_ID)
    if user_id:
        user = CMSUser.query.get(user_id)
        if user:
            g.cms_user = user

@bp.context_processor
def cms_context_processor():
    return{'CMSPermission':CMSPermission}