#coding:utf8
from flask import url_for, render_template, redirect, flash, session, request
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from . import home
from app import db
from app.home.forms import *
from app.models import User,UserLog,Preview,Tag,Movie,Comment,MovieCol
from .extra_func import *
import uuid
import os
import json

from app import create_app
app = create_app('default')
app.app_context().push()

@home.route('/login/',methods=["GET","POST"])
def login():
    form = LoginForm(name=session.get("user",None))
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data["name"]).first()
        if not user.check_pwd(data["pwd"]):
            flash("密码错误!", "err")
            return redirect(url_for('home.login'))
        session["user"] = data["name"]
        session["user_id"] = user.id
        # 管理员登录日志
        userlog = UserLog(
            user_id=session["user_id"],
            ip=request.remote_addr
        )
        db.session.add(userlog)
        db.session.commit()
        return redirect(url_for('home.user'))
    return render_template('home/login.html',form=form)

"""会员注销"""
@home.route('/logout/')
@user_login_req
def logout():
    session.pop("user", None)
    session.pop("user_id", None)
    return redirect(url_for('home.login'))

"""会员注册"""
@home.route('/register/',methods=["GET","POST"])
def register():
    form = RegistForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name = data["name"],
            email = data["email"],
            phone = data["phone"],
            pwd = generate_password_hash(data["pwd"]),
            uuid = uuid.uuid4().hex
        )
        db.session.add(user)
        db.session.commit()
        flash("注册成功！","ok")
    return render_template('home/register.html',form=form)

"""会员资料修改"""
@home.route('/user/',methods=["GET","POST"])
@user_login_req
def user():
    form = UserDetailForm()
    user = User.query.get(int(session["user_id"]))
    form.face.validators = []
    if request.method == "GET":
        form.name.data = user.name
        form.email.data = user.email
        form.phone.data = user.phone
        form.info.data = user.info
    if form.validate_on_submit():
        data = form.data
        face_url = secure_filename(form.face.data.filename)
        # 如果目录不存在，则创建并给与读写权限
        if not os.path.exists(app.config["UP_DIR"]):
            os.mkdir(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], "rw")
        face = change_filename(face_url)
        form.face.data.save(app.config["UP_DIR"]+str("users/") + face)
        name_count = User.query.filter_by(name=data["name"])
        if name_count == 1:
            flash("昵称已经存在！","err")
            return redirect(url_for('home.user'))
        user.name = data["name"]
        email_count = User.query.filter_by(email=data["email"])
        if  email_count == 1:
            flash("邮箱已经存在！", "err")
            return redirect(url_for('home.user'))
        user.email = data["email"]
        phone_count = User.query.filter_by(phone=data["phone"])
        if phone_count == 1:
            flash("手机号码已经存在！", "err")
            return redirect(url_for('home.user'))
        user.phone = data["phone"]
        user.face=face,
        user.info=data["info"],
        db.session.add(user)
        db.session.commit()
        flash("修改成功！","ok")
        return redirect(url_for('home.user'))
    return render_template('home/user.html',form=form,user=user)

@home.route('/pwd/',methods=["GET","POST"])
@user_login_req
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.get(int(session["user_id"]))
        if not user.check_pwd(data["old_pwd"]):
            flash("旧密码错误！","err")
            return redirect(url_for('home.pwd'))
        user.pwd = generate_password_hash(data["pwd"])
        db.session.add(user)
        db.session.commit()
        flash("密码修改成功！","ok")
        return redirect(url_for('home.login'))
    return render_template('home/pwd.html',form=form)

@home.route('/comment/<int:page>/',methods=["GET"])
@user_login_req
def comment(page=None):
    if page is None:
        page = 1
    page_data = Comment.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == Comment.movie_id,
        User.id == session["user_id"]
    ).order_by(Comment.addtime.desc()).paginate(page=page,per_page=10)
    return render_template('home/comment.html',page_data=page_data)

@home.route('/loginlog/<int:page>/',methods=["GET"])
@user_login_req
def loginlog(page=None):
    if page is None:
        page = 1
    page_data = UserLog.query.filter(
        UserLog.user_id ==int(session["user_id"])
    ).paginate(page=page, per_page=10)
    return render_template('home/loginlog.html',page_data=page_data)

@home.route('/moviecol/add/',methods=["GET"])
@user_login_req
def moviecol_add():
    mid = request.args.get("mid",None)
    uid = request.args.get("uid",None)
    moviecol_count = MovieCol.query.filter_by(
        user_id=int(uid),
        movie_id=int(mid)
    ).count()
    if  moviecol_count == 1:
        data=dict(ok=0)
    else:
        moviecol = MovieCol(
            user_id=int(uid),
            movie_id=int(mid)
        )
        db.session.add(moviecol)
        db.session.commit()
        data=dict(ok=0)
    return json.dumps(data)

@home.route('/moviecol/<int:page>',methods=["GET"])
@user_login_req
def moviecol(page=None):
    if page is None:
        page = 1
    page_data = MovieCol.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == MovieCol.movie_id,
        User.id == session["user_id"]
    ).order_by(MovieCol.addtime.desc()).paginate(page=page,per_page=10)
    return render_template('home/moviecol.html',page_data=page_data)

@home.route('/')
@home.route('/<int:page>',methods=["GET","POST"])
def index(page=None):
    tags = Tag.query.all()
    page_data = Movie.query
    #标签
    tid = request.args.get("tid", 0)
    if int(tid) != 0:
        page_data = page_data.filter_by(tag_id=int(tid))
    # 星级
    star = request.args.get("star", 0)
    if int(star) != 0:
        page_data = page_data.filter_by(star=int(star))
    # 时间
    time = request.args.get("time", 0)
    if int(time) != 0:
        if int(time) ==1:
            page_data = page_data.order_by(Movie.addtime.desc())
        else:
            page_data = page_data.order_by(Movie.addtime.asc())
    # 播放量
    pm = request.args.get("pm", 0)
    if int(pm) != 0:
        if int(time) ==1:
            page_data = page_data.order_by(Movie.playnum.desc())
        else:
            page_data = page_data.order_by(Movie.playnum.asc())
    # 评论量
    cm = request.args.get("cm", 0)
    if int(cm) != 0:
        if int(time) ==1:
            page_data = page_data.order_by(Movie.commentnum.desc())
        else:
            page_data = page_data.order_by(Movie.commentnum.asc())
    cf = dict(
        tid=tid,
        star=star,
        time=time,
        pm=pm,
        cm=cm,
    )
    if page is None:
        page = 1
    page_data = page_data.paginate(page=page, per_page=10)
    return render_template('home/index.html',tags=tags,cf=cf,page_data=page_data)

"""上映预告"""
@home.route('/animation/',methods=["GET"])
def animation():
    data = Preview.query.all()
    return render_template('home/animation.html',data=data)

@home.route('/search/<int:page>',methods=["GET"])
def search(page=None):
    if page is None:
        page = 1
    key = request.args.get("key",None)
    movie_count = Movie.query.filter(
        Movie.title.ilike('%'+key+'%')
    ).count()
    page_data = Movie.query.filter(
        Movie.title.ilike('%'+key+'%')
    ).paginate(page=page, per_page=10)
    return render_template('home/search.html',key=key,movie_count=movie_count,page_data=page_data)

@home.route('/play/<int:id>/<int:page>/',methods=["GET","POST"])
def play(id=None,page=None):
    #获取对应id的电影和标签
    movie = Movie.query.join(
        Tag
    ).filter(
        Tag.id == Movie.tag_id,
        Movie.id == int(id)
    ).first_or_404()
    #评论分页
    if page is None:
        page = 1
    page_data = Comment.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == movie.id,
        User.id == Comment.user_id
    ).order_by(Comment.addtime.desc()).paginate(page=page,per_page=10)
    #播放数量加1
    movie.playnum = movie.playnum + 1
    form = CommentForm()
    if "user" in session and form.validate_on_submit():
        data = form.data
        comment = Comment(
            content=data["content"],
            movie_id=movie.id,
            user_id=session["user_id"]
        )
        db.session.add(comment)
        db.session.commit()
        # 评论数量加1
        movie.commentnum = movie.commentnum + 1
        db.session.add(movie)
        db.session.commit()
        flash("评论成功!","ok")
        return redirect(url_for('home.play',id=movie.id,page=1))
    db.session.add(movie)
    db.session.commit()
    return render_template('home/play.html',movie=movie,form=form,page_data=page_data)


