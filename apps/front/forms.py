from apps.forms import BaseForm
from wtforms import StringField,BooleanField,IntegerField
from wtforms.validators import Regexp,InputRequired,EqualTo,Length,ValidationError
from utils import cms_memcache

class SignupForm(BaseForm):
    telephone = StringField(validators=[Regexp(r"1[345789]\d{9}",message='请输入正确的手机号码！')])
    username = StringField(validators=[Length(min=2,max=20,message='用户名长度为2-20个字符！')])
    password1 = StringField(validators=[Length(min=6,max=20,message='密码长度为6-20个字符！')])
    password2 = StringField(validators=[EqualTo('password1',message='两次密码不相等')])
    graph_captcha = StringField(validators=[Regexp(r"[0-9a-zA-Z]{4}",message='验证码格式错误！')])

    def validate_graph_captcha(self,field):
        graph_captcha = field.data
        graph_captcha_mem = cms_memcache.get('captcha')
        if not graph_captcha_mem:
            raise ValidationError('图形验证码发生错误')
        if graph_captcha.lower() != graph_captcha_mem.lower():
            raise ValidationError('验证码错误')

class LoginForm(BaseForm):
    telephone = StringField(validators=[Regexp(r"1[345789]\d{9}", message='请输入正确的手机号码！')])
    password = StringField(validators=[Length(min=6,max=20,message='密码长度为6-20个字符！')])
    graph_captcha = StringField(validators=[Regexp(r"[0-9a-zA-Z]{4}", message='验证码格式错误！')])
    remember = BooleanField()

    def validate_graph_captcha(self, field):
        graph_captcha = field.data
        graph_captcha_mem = cms_memcache.get('captcha')
        if not graph_captcha_mem:
            raise ValidationError('图形验证码发生错误')
        if graph_captcha.lower() != graph_captcha_mem.lower():
            raise ValidationError('验证码错误')

class AddPostForm(BaseForm):
    title = StringField(validators=[InputRequired(message='请输入标题！')])
    content = StringField(validators=[InputRequired(message='请输入内容！')])
    board_id = IntegerField(validators=[InputRequired(message='请输入板块ID！')])

class AddCommentForm(BaseForm):
    content = StringField(validators=[InputRequired(message='请输入内容！')])
    post_id = IntegerField(validators=[InputRequired(message='系统没有获取到帖子ID！')])
    author_id = StringField(validators=[InputRequired(message='系统没有获取到用户ID不！')])
