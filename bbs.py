from flask import Flask,views,render_template,request
from flask_wtf import CSRFProtect
from apps.cms  import bp as cms_bp
from apps.common import bp as common_bp
from apps.front import bp as front_bp
from apps.ueditor import bp as ueditor_bp
import config
from exts import db,mail


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    mail.init_app(app)
    app.register_blueprint(ueditor_bp)
    app.register_blueprint(cms_bp)
    app.register_blueprint(common_bp)
    app.register_blueprint(front_bp)
    CSRFProtect(app)
    return app
app = create_app()
if __name__ == '__main__':
    app.run()
