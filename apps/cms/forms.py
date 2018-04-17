from wtforms import StringField,BooleanField,IntegerField
from wtforms.validators import Email,Length,InputRequired,EqualTo,ValidationError
from apps.forms import BaseForm
from utils import cms_memcache
from flask import g
import re

class LoginForm(BaseForm):
    email = StringField(validators=[Email(message="邮箱格式不正确"), InputRequired(message="邮箱不能为空")])
    password = StringField(validators=[Length(min=6, message="密码至少为6位"),InputRequired(message="密码不能为空")])
    remember = BooleanField()

class ResetpwdForm(BaseForm):
    oldpassword = StringField(validators=[Length(min=6, message="密码至少为6位")])
    newpassword1 = StringField(validators=[Length(min=6, message="密码至少为6位")])
    newpassword2 = StringField(validators=[EqualTo("newpassword1",message="两次输入不一样")])

class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message="邮箱格式不正确！")])
    captcha = StringField(validators=[Length(min=6,max=6,message="验证码为6位！")])
    def validate_captcha(self,field):
        captcha = field.data
        email = self.email.data
        captcha_chache = cms_memcache.get(email)
        if captcha_chache and captcha == captcha:
            return True
        else:
            raise ValidationError('邮件验证码错误')

    def validate_email(self,field):
        email = field.data
        user = g.cms_user
        if user.email == email:
            raise ValidationError('你确定你在修改邮箱！')

def validate_email(email):
    r = re.compile("^[a-zA-Z0-9_]+@[a-zA-Z0-9_]+\.[a-zA-Z]{1,4}$")
    if re.match(r, email):
        return True
    return False

class AddBannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入轮播图片名称！')])
    image_url = StringField(validators=[InputRequired(message='请输入轮播图片链接！')])
    link_url = StringField(validators=[InputRequired(message='请输入轮播图片跳转链接！')])
    priority = IntegerField(validators=[InputRequired(message='请输入轮播图片优先级！')])
    id = StringField()

class AddBoardForm(BaseForm):
    name = StringField(validators=[InputRequired('请输入板块名称！')])
    id = StringField()