from flask import Blueprint,render_template,views,request,redirect,url_for,session,g,jsonify
from .forms import LoginForm,ResetpwdForm,ResetEmailForm,validate_email,AddBannerForm,AddBoardForm
from .models import CMSUser
import config
from .decorators import login_required
from exts import db,mail
from utils import restful,cms_memcache
from flask_mail import Message
import string,random
from ..models import BannerModel,BoardModel,PostModel,HighlightPostModel
from flask_paginate import Pagination,get_page_parameter


bp = Blueprint('cms',__name__,url_prefix='/cms')

#cms首页
@bp.route('/')
@login_required
def cms_index():
    return render_template("cms/cms_index.html")

#登录视图函数
class LoginView(views.MethodView):
    def get(self,message=None):
        return render_template('cms/login.html',message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            passowrd = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(passowrd):
                session[config.CMS_USER_ID] = user.id
                if remember:
                    session.permanent = True
                return restful.success()
            else:
                return restful.params_error(message="邮箱或者密码错误,请重新输入!")
        else:

            return restful.params_error(message="邮箱或者密码格式错误,请重新输入!")
bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))

#注销
@bp.route('/logout/')
@login_required
def logout():
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))

#个人中心
@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_profile.html')

#修改密码
class RestPasswordView(views.MethodView):
    decorators = [login_required]
    def get(self,message=None):
        return render_template("cms/cms_resetpwd.html")
    def post(self):
        form = ResetpwdForm(request.form)
        if form.validate():
            oldpassword = form.oldpassword.data
            user = g.cms_user
            if user and user.check_password(oldpassword):
                newpassword = form.newpassword1.data
                user.password = newpassword
                db.session.commit()
                return restful.success(message="密码修改成功！")
            else:
                return restful.params_error(message="旧密码错误！")
        else:
            return restful.params_error(message="密码格式错误！")
bp.add_url_rule('/resetpwd/', view_func=RestPasswordView.as_view('resetpwd'))

#修改邮箱
class ResetEmailView(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            user = g.cms_user
            user.email = email
            db.session.commit()
            return restful.success(message="邮箱修改成功")
        else:
             message = form.get_error()
             return restful.params_error(message=message)
bp.add_url_rule('/resetemail/',view_func=ResetEmailView.as_view('resetemail'))

#发送验证码
@bp.route('/email_captcha/')
def email_captcha():
    email = request.args.get('email')
    if not validate_email(email):
        return restful.params_error(message='邮箱格式错误')
    if email == g.cms_user.email:
        return restful.params_error(message='要修改的邮箱和原邮箱一致，你确定是要修改邮箱')
    source = list(string.ascii_lowercase) + list(string.digits)
    captcha = "".join(random.sample(source, 6))
    body = '您的验证码是：%s' % captcha
    message = Message('CMS管理后台邮件发送', recipients=[email], body=body)
    cms_memcache.set(email,captcha)
    try:
        mail.send(message=message)
    except:
        return restful.server_error()
    return restful.success(message="邮件发送成功请注意查收！")

#帖子管理
@bp.route('/posts/')
@login_required
def posts():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    PER_PAGE  = config.CMS_PER_PAGE
    start = (page-1)*PER_PAGE
    end = start+PER_PAGE
    query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    posts = query_obj.slice(start,end)
    total = query_obj.count()
    pagination = Pagination(page=page,total=total,bs_version=3)
    context = {
        'posts': posts,
        'pagination': pagination
    }
    return render_template('cms/cms_posts.html',**context)

#帖子加精
@bp.route('/hpost/',methods=['POST'])
@login_required
def hpost():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.params_error('此帖子ID不存在')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error('未找到此帖子')
    is_h = HighlightPostModel.query.filter_by(post_id=post_id).all()
    if is_h:
        return restful.success('此贴已经加精！')
    highlight = HighlightPostModel(post_id=post_id)
    db.session.add(highlight)
    db.session.commit()
    return restful.success('加精成功！')

#帖子取消加精
@bp.route('/uhpost/',methods=['POST'])
@login_required
def uhpost():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.params_error('此帖子ID不存在')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error('未找到此帖子')
    highlight = post.highlight
    for h in highlight:
        db.session.delete(h)
    db.session.commit()
    return restful.success('取消加精成功！')

#评论管理
@bp.route('/comments/')
@login_required
def comments():
    return render_template('cms/cms_comments.html')

#板块管理
@bp.route('/boards/')
@login_required
def boards():
    boards = BoardModel.query.all()
    return render_template('cms/cms_boards.html',boards=boards)

#添加板块
@bp.route('/aboard/',methods=['POST'])
@login_required
def aboard():
    form = AddBoardForm(request.form)
    if form.validate():
        name = form.name.data
        board = BoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success('板块添加成功！')

#修改板块
@bp.route('/uboard/',methods=['POST'])
@login_required
def uboard():
    form = AddBoardForm(request.form)
    if form.validate():
        name = form.name.data
        id = form.id.data
        board = BoardModel.query.get(id)
        if board:
            board.name = name
            db.session.commit()
            return restful.success('板块修改成功！')
        else:
            return restful.params_error('此板块ID未查询到！')

#删除板块
@bp.route('/dboard/',methods=['POST'])
@login_required
def dboard():
    form = request.form
    id = form.get('id')
    board = BoardModel.query.get(id)
    if board:
        db.session.delete(board)
        db.session.commit()
        return restful.success('板块删除成功！')
    else:
        return restful.params_error('删除失败，此板块ID未查询到！')


#轮播图管理
@bp.route('/banners/')
@login_required
def banners():
    banners = BannerModel.query.order_by(BannerModel.priority.desc())
    return render_template('cms/cms_banners.html',banners=banners)


#轮播图添加
@bp.route('/abanners/',methods=['POST'])
@login_required
def abanners():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel(name=name,image_url=image_url,link_url=link_url,priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success('轮播图信息添加成功！')
    else:
        return restful.params_error(form.get_error())


#轮播图修改
@bp.route('/ubanners/',methods=['POST'])
@login_required
def ubanners():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        id = form.id.data
        banner = BannerModel.query.get(id)

        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success('轮播图信息修改成功！')
        else:
            return restful.server_error('没有这个轮播图')
    else:
        return restful.params_error(form.get_error())


#轮播图删除
@bp.route('/dbanners/',methods=['GET'])
@login_required
def dbanners():
    id = request.args.get('id')
    banner = BannerModel.query.get(id)
    if banner:
        db.session.delete(banner)
        db.session.commit()
        return restful.success('轮播图删除成功！')
    else:
        return restful.params_error('未查询到此轮播图ID！')


@bp.route('/fusers/')
@login_required
def fusers():
    return render_template('cms/cms_fusers.html')


@bp.route('/cusers/')
@login_required
def cusers():
    return render_template('cms/cms_cusers.html')


@bp.route('/croles/')
@login_required
def croles():
    return render_template('cms/cms_croles.html')

