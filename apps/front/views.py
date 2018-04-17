from flask import  Blueprint,views,render_template,url_for,make_response,g,request,session,redirect,abort
from utils.captcha import Captcha
from utils import cms_memcache,restful
from .forms import SignupForm,LoginForm,AddPostForm,AddCommentForm
from .models import FrontUser
from exts import db
from .decorators import login_required
from config import FRONT_USER_ID,PER_PAGE
from ..models import BannerModel,BoardModel,PostModel,CommentModel
from io import BytesIO
from flask_paginate import Pagination,get_page_parameter

bp = Blueprint('front',__name__)

#首页视图函数
@bp.route('/')
def index():
    board_id = request.args.get('bd',type=int,default=None)
    page = request.args.get(get_page_parameter(),type=int,default=1)
    start = (page-1)*PER_PAGE
    end = start + PER_PAGE
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
    boards = BoardModel.query.all()

    if board_id:
        query_obj = PostModel.query.filter_by(board_id=board_id)
    else:
        query_obj = PostModel.query
    posts = query_obj.slice(start, end)
    total = query_obj.count()
    pagination = Pagination(page=page,total=total,bs_version=3)

    context = {
        'banners':banners,
        'boards':boards,
        'posts':posts,
        'pagination':pagination
    }
    return render_template('front/front_index.html',**context)

#注册视图函数
class SignupView(views.MethodView):
    def get(self):
        return_to = request.referrer
        return render_template('front/front_signup.html', return_to=return_to)
    def post(self):
        form = SignupForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password1.data
            user = FrontUser(telephone=telephone,username=username,password=password)
            db.session.add(user)
            db.session.commit()
            return restful.success(message='注册成功  ')
        else:
            message = form.get_error()
            print('message:',message)
            return restful.params_error(message=message)

#登录视图函数
class LoginView(views.MethodView):
    def get(self):
        return_to = request.referrer
        current_url = request.url
        return render_template('front/front_login.html',return_to=return_to)
    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data
            user = FrontUser.query.filter_by(telephone=telephone).first()
            if user:
                if user.check_password(password):
                    session[FRONT_USER_ID] = user.id
                    if 1:
                        session.permanent = True
                    return restful.success()
                else:
                    return restful.params_error('密码错误')
            else:
                return restful.params_error('此手机号码未注册！')

        else:
            return restful.params_error(message=form.get_error())

#注销视图函数
@bp.route('/logout/')
@login_required
def logout():
   session.clear()
   return redirect(url_for('front.index'))

#生成验证码
@bp.route('/captcha/')
def gene_captcha():
    text,image = Captcha.gene_graph_captcha()
    cms_memcache.set('captcha',text,timeout=600)
    print('captcha:',cms_memcache.get('captcha'))
    out = BytesIO()
    image.save(out,'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp

#检测验证码
@bp.route('/captcha/check/')
def check_captcha():
    print('get captcha:',cms_memcache.get('captcha'))
    cap_val = request.args.get('cap_val')
    if cap_val.lower() == cms_memcache.get('captcha').lower():
        return restful.success()
    else:
        return restful.params_error()

#添加帖子视图函数
class ApostView(views.MethodView):
    decorators = [login_required]
    def get(self):
        boards = BoardModel.query.all()
        return render_template('front/front_apost.html',boards=boards)

    def post(self):
        form = AddPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            post = PostModel(title=title,content=content,board_id=board_id)
            post.author = g.front_user
            db.session.add(post)
            db.session.commit()
            return restful.success('帖子发布成功！')
        else:
            return restful.params_error(form.get_error())

#帖子详情页面
@bp.route('/p/<post_id>')
def post_detail(post_id):
    post = PostModel.query.get(post_id)
    if post:
        comments = CommentModel.query.filter(CommentModel.post_id == post_id).order_by(CommentModel.create_time.desc())
        context = {
            'post':post,
            'comments':comments
        }
        return render_template('front/front_post_detail.html',**context)
    else:
        abort(404)

#发表评论
@bp.route('/acomment/',methods=['Post'])
@login_required
def add_comment():
    form = AddCommentForm(request.form)
    if form.validate():
        content = form.content.data
        post_id = form.post_id.data
        author_id = form.author_id.data
        print('comment content:',content)
        print('post id:',post_id)
        print('comment author id:',author_id)
        comment = CommentModel(content=content,post_id=post_id,author_id=author_id)
        db.session.add(comment)
        db.session.commit()
        return restful.success('评论发表成功！')
    else:
        return restful.params_error(form.get_error())






bp.add_url_rule('/signup/',view_func=SignupView.as_view('signup'))
bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))
bp.add_url_rule('/apost/',view_func=ApostView.as_view('apost'))

