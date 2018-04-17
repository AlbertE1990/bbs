from flask_migrate import Migrate,MigrateCommand
from bbs import app
from exts import db
from flask_script import Manager
from apps.cms import models as cms_models
from apps.front import models as front_models
import apps.models as models
from random import random,choice,randint,randrange

CMSPermission = cms_models.CMSPermission
CMSRole = cms_models.CMSRole
CMSUser = cms_models.CMSUser
FrontUser = front_models.FrontUser

manager = Manager(app)
Migrate(app,db)
manager.add_command('db',MigrateCommand)


@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-e','--email',dest='email')
def create_cms_user(username,password,email):
    user = CMSUser(username=username,password=password,email=email)
    db.session.add(user)
    db.session.commit()
    print("CMS用户添加成功")


@manager.command
def create_role():

    #1.访问者（修改个人信息）
    vistor = CMSRole(name='访问者',desc='只能访问相关数据')
    vistor.permissions = CMSPermission.VISTOR

    #2.运营员（修改个人信息，管理帖子，管理评论，管理前台用户）
    operator = CMSRole(name='运营员',desc='修改个人信息，管理帖子，管理评论，管理前台用户')
    operator.permissions = CMSPermission.VISTOR | CMSPermission.POSTER | \
                           CMSPermission.COMMENTER|CMSPermission.FRONTUSER


    #3.管理人员
    admin = CMSRole(name='管理员',desc='拥有本系统所有权限')
    admin.permissions = CMSPermission.VISTOR | CMSPermission.POSTER |\
                        CMSPermission.COMMENTER|CMSPermission.FRONTUSER |\
                        CMSPermission.BOARDER | CMSPermission.CMSUSER

    #4.开发者
    developer = CMSRole(name='开发者', desc='所有权限，开发者专用')
    developer.permissions = CMSPermission.ALL_PERMISSION

    db.session.add_all([vistor,operator,admin,developer])
    db.session.commit()


@manager.option('-e','--email',dest='email')
@manager.option('-n','--name',dest='name')
def add_user_to_role(email,name):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            user.roles.append(role)
            db.session.commit()
            print('用户添加角色成功！')
        else:
            print('没有这个角色%s！'%name)
    else:
        print('此邮箱：%s 没有注册！'%email)


@manager.option('-t','--telephone',dest='telephone')
@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
def create_front_user(telephone,username,password):
    fuser = FrontUser(telephone=telephone,username=username,password=password)
    db.session.add(fuser)
    db.session.commit()
    print('前台账号创建成功')

@manager.command
def create_posts():
    for i in range(100):
        user = choice(FrontUser.query.all())
        board = choice(models.BoardModel.query.all())
        author_id = user.id
        board_id = board.id
        title = "测试标题%d"%(i+10)
        content = "测试内容%d"%(i+10)
        post = models.PostModel(title=title,content=content,board_id=board_id,author_id=author_id)
        db.session.add(post)
        db.session.commit()
    print('添加数据成功！')

@manager.command
def create_comments():
    posts =  models.PostModel.query.all()
    i=0
    for post in posts:
        post_id = post.id
        for i in range(30):
            user = choice(FrontUser.query.all())
            author_id = user.id
            content = "测试内容评论来,自动填充%d" % (i)
            comment = models.CommentModel(content=content,post_id=post_id,author_id=author_id)
            db.session.add(comment)
        db.session.commit()
    print('添加数据成功！')

if __name__ == '__main__':
    manager.run()