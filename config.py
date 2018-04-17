import os

#db
DB_USERNAME = 'root'
DB_PASSWORD = 'root'
DB_HOST     = 'localhost'
DB_PORT     = '3306'
DB_NAME     = 'bbs'
DB_URI      = "mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8"%\
         (DB_USERNAME,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False


DEBUG = True
SECRET_KEY = os.urandom(24)
CMS_USER_ID = "helloword"
FRONT_USER_ID = "frontabc"

#mail
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = '587'
MAIL_USE_TLS = True
#MAIL_USE_SSL = True
MAIL_USERNAME = "112288349@qq.com"
MAIL_PASSWORD = "kgqembbxywxfcbbb"
MAIL_DEFAULT_SENDER = "112288349@qq.com"

#UEditor相关配置
UEDITOR_UPLOAD_PATH = os.path.join(os.path.dirname(__file__),'images')


#翻页配置 flask-pagination

PER_PAGE = 10
CMS_PER_PAGE = 15