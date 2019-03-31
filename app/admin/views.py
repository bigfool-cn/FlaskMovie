#coding:utf8
from flask import render_template,redirect,url_for,flash,session,request
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from app.admin.forms import *
from . import admin
from app.models import *
from .extra_func import *
import os

"""首页"""
@admin.route('/')
@admin_login_req
def index():
    return render_template('admin/index.html')

"""登陆"""
@admin.route('/login/',methods=['GET','POST'])
def login():
    form = LoginForm(account=session.get("admin",None))
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=data["account"]).first()
        if not admin.check_pwd(data["pwd"]):
            flash("密码错误!","err")
            return  redirect(url_for('admin.login'))
        session["admin"] = data["account"]
        session["user_id"] = admin.id
        #管理员登录日志
        adminlog = AdminLog(
            admin_id = session["user_id"],
            ip = request.remote_addr
        )
        db.session.add(adminlog)
        db.session.commit()
        return redirect(request.args.get("next") or url_for('admin.index'))
    return render_template('admin/login.html',form=form)

"""退出"""
@admin.route('/logout/')
@admin_login_req
def logout():
    session.pop("admin",None)
    session.pop("user_id",None)
    return redirect(url_for('admin.login'))

"""修改密码"""
@admin.route('/pwd/',methods=["GET","post"])
@admin_login_req
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        name = session["admin"]
        admin = Admin.query.filter_by(name=name).first()
        admin.pwd = generate_password_hash(data["new_pwd"])
        db.session.add(admin)
        db.session.commit()
        flash("修改密码成功，请重新登陆！","ok")
        #记录操作日志
        oplog = OpLog(
            user_id = session["user_id"],
            ip = request.remote_addr, #获取登陆ip,
            reason = "修改了密码"
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('admin.logout'))
    return render_template('admin/pwd.html',form=form)

"""添加标签"""
@admin.route('/tag/add/',methods=["GET","POST"])
@admin_login_req
@admin_auth
def tag_add():
    form= TagForm()
    if form.validate_on_submit():
        data = form.data
        tag_count = Tag.query.filter_by(name=data["name"]).count()
        if tag_count == 1:
            flash("标签名称已存在","err")
            return redirect(url_for('admin.tag_add'))
        tag = Tag(name=data["name"])
        db.session.add(tag)
        db.session.commit()
        flash("标签添加成功","ok")
        # 记录操作日志
        oplog = OpLog(
            user_id=session["user_id"],
            ip=request.remote_addr,  # 获取登陆ip,
            reason="添加了一个标签：%s" %data["name"]
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('admin.tag_add'))
    return render_template('admin/tag_add.html',form=form)

"""标签列表"""
@admin.route('/tag/list/<int:page>/',methods=["GET"])
@admin_login_req
@admin_auth
def tag_list(page=None):
    if page is None:
        page = 1
    page_data = Tag.query.order_by(Tag.addtime.desc()).paginate(page=page,per_page=10)
    return render_template('admin/tag_list.html',page_data=page_data)

"""标签列修改"""
@admin.route('/tag/edit/<int:id>/',methods=["GET","POST"])
@admin_login_req
@admin_auth
def tag_edit(id=None):
    form = TagForm()
    tag = Tag.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        tag_count = Tag.query.filter_by(name=data["name"]).count()
        if tag_count == 1 and tag.name != data["name"]:
            flash("标签名称已存在", "err")
            return redirect(url_for('admin.tag_edit',id=id))
        tag.name=data["name"]
        db.session.add(tag)
        db.session.commit()
        flash("修改标签成功", "ok")
        # 记录操作日志
        oplog = OpLog(
            user_id=session["user_id"],
            ip=request.remote_addr,  # 获取登陆ip,
            reason="修改标签了：%s→%s" %(tag.name,data["name"])
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('admin.tag_edit',id=id))
    return render_template('admin/tag_edit.html', form=form,tag=tag)

"""标签删除"""
@admin.route('/tag/del/<int:id>/',methods=["GET"])
@admin_login_req
@admin_auth
def tag_del(id=None):
    tag = Tag.query.filter_by(id=id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash("标签删除成功","ok")
    # 记录操作日志
    oplog = OpLog(
        user_id=session["user_id"],
        ip=request.remote_addr,  # 获取登陆ip,
        reason="删除了一个标签：%s" %tag.name
    )
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for("admin.tag_list",page=1))

"""添加电影"""
@admin.route('/movie/add/',methods=["GET","POST"])
@admin_login_req
@admin_auth
def movie_add():
    form = MovieForm()
    if form.validate_on_submit():
        data = form.data
        movie_url = secure_filename(form.url.data.filename)
        logo_url = secure_filename(form.logo.data.filename)
        #如果目录不存在，则创建并给与读写权限
        if not os.path.exists(app.config["UP_DIR"]):
            os.mkdir(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"],"rw")
        url = change_filename(movie_url)
        logo = change_filename(logo_url)
        form.url.data.save(app.config["UP_DIR"] + url)
        form.logo.data.save(app.config["UP_DIR"] + logo)
        movie = Movie(
            title=data["title"],
            url=url,
            info=data["info"],
            logo=logo,
            star=int(data["star"]),
            playnum=0,
            commentnum=0,
            tag_id=int(data["tag_id"]),
            area=data["area"],
            release_time=data["release_time"],
            length=data["length"],
        )
        db.session.add(movie)
        db.session.commit()
        flash("电影添加成功","ok")
        # 记录操作日志
        oplog = OpLog(
            user_id=session["user_id"],
            ip=request.remote_addr,  # 获取登陆ip,
            reason="添加了一部电影：%s" %data["title"]
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for("admin.movie_add"))
    return render_template('admin/movie_add.html',form=form)

"""电影列表"""
@admin.route('/movie/list/<int:page>',methods=["GET"])
@admin_login_req
@admin_auth
def movie_list(page=None):
    if page is None:
        page = 1
    #关联查询
    page_data = Movie.query.join(Tag).filter(Tag.id == Movie.tag_id).order_by(Movie.addtime.desc()).paginate(page=page,per_page=10)
    return render_template('admin/movie_list.html',page_data=page_data)

"""修改电影"""
@admin.route('/movie/edit/<int:id>/',methods=["GET","POST"])
@admin_login_req
@admin_auth
def movie_edit(id=None):
    form = MovieForm()
    form.url.validators = []
    form.logo.validators = []
    movie= Movie.query.get_or_404(id)
    if request.method == "GET":
        form.info.data = movie.info
        form.tag_id.data = movie.tag_id
        form.star.data = movie.star
    if form.validate_on_submit():
        data = form.data
        movie_count = Movie.query.filter_by(title=data["title"]).count()
        if movie_count == 1 and movie.title != data["title"]:
            flash("片名已存在", "err")
            return redirect(url_for('admin.movie_edit', id=id))
        #判断目录是否存在，不存在则创建并给与读写权限
        if not os.path.exists(app.config["UP_DIR"]):
            os.mkdir(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], "rw")
        #判断文件是否选择，选择了则更改数据库和文件信息
        if form.url.data.filename !="":
            os.remove(app.config["UP_DIR"] + str(movie.url))
            movie_url = secure_filename(form.url.data.filename)
            movie.url = change_filename(movie_url)
            form.url.data.save(app.config["UP_DIR"] + movie.url)
        if form.logo.data.filename != "":
            os.remove(app.config["UP_DIR"] + str(movie.logo))
            logo_url = secure_filename(form.logo.data.filename)
            movie.logo = change_filename(logo_url)
            form.logo.data.save(app.config["UP_DIR"] + movie.logo)
        movie.title = data["title"]
        movie.info = data["info"]
        movie.star = data["star"]
        movie.tag_id = data["tag_id"]
        movie.area = data["area"]
        movie.length = data["length"]
        movie.release_time = data["release_time"]
        db.session.add(movie)
        db.session.commit()
        flash("修改电影成功", "ok")
        # 记录操作日志
        oplog = OpLog(
            user_id=session["user_id"],
            ip=request.remote_addr,  # 获取登陆ip,
            reason="修改了电影信息：%s" %data["title"]
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('admin.movie_edit',id=id))
    return render_template('admin/movie_edit.html', form=form,movie=movie)

"""删除电影"""
@admin.route('/movie/del/<int:id>/',methods=["GET"])
@admin_login_req
@admin_auth
def movie_del(id=None):
    movie = Movie.query.get_or_404(id)
    os.remove(app.config["UP_DIR"] + str(movie.logo))
    os.remove(app.config["UP_DIR"] + str(movie.url))
    db.session.delete(movie)
    db.session.commit()
    flash("电影删除成功","ok")
    # 记录操作日志
    oplog = OpLog(
        user_id=session["user_id"],
        ip=request.remote_addr,  # 获取登陆ip,
        reason="删除了一部电影：%s" %movie.title
    )
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for("admin.movie_list",page=1))

"""预告列表"""
@admin.route('/preview/add/',methods=["GET","POST"])
@admin_login_req
@admin_auth
def preview_add():
    form = PreviewForm()
    if form.validate_on_submit():
        data = form.data
        logo_url = form.logo.data.filename
        if not os.path.exists(app.config["UP_DIR"]):
            os.mkdir(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], "rw")
        logo = change_filename(logo_url)
        form.logo.data.save(app.config["UP_DIR"] + logo)
        preview = Preview(title=data["title"],logo=logo)
        db.session.add(preview)
        db.session.commit()
        flash("添加预告成功","ok")
        # 记录操作日志
        oplog = OpLog(
            user_id=session["user_id"],
            ip=request.remote_addr,  # 获取登陆ip,
            reason="添加了一个预告：%s" % data["title"]
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('admin.preview_add'))
    return render_template('admin/preview_add.html',form=form)

"""预告列表"""
@admin.route('/preview/list/<int:page>',methods=["GET"])
@admin_login_req
@admin_auth
def preview_list(page=None):
    if page is None:
        page = 1
    page_data = Preview.query.order_by(Preview.addtime.desc()).paginate(page=page,per_page=10)
    return render_template('admin/preview_list.html',page_data=page_data)

"""修改预告"""
@admin.route('/preview/edit/<int:id>',methods=["GET","POST"])
@admin_login_req
@admin_auth
def preview_edit(id=None):
    form = PreviewForm()
    form.logo.validators = []
    preview= Preview.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        preview_count = Preview.query.filter_by(title=data["title"]).count()
        if preview_count == 1 and preview.title != data["title"]:
            flash("预告已存在", "err")
            return redirect(url_for('admin.preview_edit', id=id))
        #判断目录是否存在，不存在则创建并给与读写权限
        if not os.path.exists(app.config["UP_DIR"]):
            os.mkdir(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], "rw")
        #判断文件是否选择，选择了则更改数据库和文件信息
        if form.logo.data.filename != "":
            os.remove(app.config["UP_DIR"] + str(preview.logo))
            logo_url = secure_filename(form.logo.data.filename)
            preview.logo = change_filename(logo_url)
            form.logo.data.save(app.config["UP_DIR"] + preview.logo)
        preview.title = data["title"]
        db.session.add(preview)
        db.session.commit()
        flash("修改预告成功", "ok")
        # 记录操作日志
        oplog = OpLog(
            user_id=session["user_id"],
            ip=request.remote_addr,  # 获取登陆ip,
            reason="修改了一个预告：%s→%s" %(preview.title,data["title"])
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('admin.preview_edit',id=id))
    return render_template('admin/preview_edit.html', form=form,preview=preview)

"""删除预告"""
@admin.route('/preview/del/<int:id>/',methods=["GET"])
@admin_login_req
@admin_auth
def preview_del(id=None):
    preview = Preview.query.get_or_404(id)
    os.remove(app.config["UP_DIR"]+str(preview.logo))
    db.session.delete(preview)
    db.session.commit()
    flash("预告删除成功","ok")
    # 记录操作日志
    oplog = OpLog(
        user_id=session["user_id"],
        ip=request.remote_addr,  # 获取登陆ip,
        reason="删除了一个预告：%s" %preview.title
    )
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for("admin.preview_list",page=1))

"""会员列表"""
@admin.route('/user/list/<int:page>',methods=["GET"])
@admin_login_req
@admin_auth
def user_list(page=None):
    if page is None:
        page = 1
    page_data = User.query.order_by(User.addtime.desc()).paginate(page=page,per_page=10)
    return render_template('admin/user_list.html',page_data=page_data)
    return render_template('admin/user_list.html')

"""查看会员"""
@admin.route('/user/view/<int:id>',methods=["GET"])
@admin_login_req
@admin_auth
def user_view(id=None):
    user = User.query.get_or_404(id)
    return render_template('admin/user_view.html',user=user)

"""删除会员"""
@admin.route('/user/del/<int:id>/',methods=["GET"])
@admin_login_req
@admin_auth
def user_del(id=None):
    user = User.query.get_or_404(id)
    os.remove(app.config["UP_DIR"]+"users/"+str(user.face))
    db.session.delete(user)
    db.session.commit()
    flash("会员删除成功","ok")
    # 记录操作日志
    oplog = OpLog(
        user_id=session["user_id"],
        ip=request.remote_addr,  # 获取登陆ip,
        reason="删除了一个会员：%s" %user.name
    )
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for("admin.user_list",page=1))

"""评论列表"""
@admin.route('/comment/list/<int:page>',methods=["GET"])
@admin_login_req
@admin_auth
def comment_list(page=None):
    if page is None:
        page = 1
    page_data = Comment.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == Comment.movie_id,
        User.id == Comment.user_id
    ).order_by(Comment.addtime.desc()).paginate(page=page,per_page=10)
    return render_template('admin/comment_list.html',page_data=page_data)

"""删除评论"""
@admin.route('/comment/del/<int:id>/',methods=["GET"])
@admin_login_req
@admin_auth
def comment_del(id=None):
    comment = Comment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    flash("评论删除成功","ok")
    # 记录操作日志
    oplog = OpLog(
        user_id=session["user_id"],
        ip=request.remote_addr,  # 获取登陆ip,
        reason="删除了一条评论：%s" %comment.content
    )
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for("admin.comment_list",page=1))

"""收藏列表"""
@admin.route('/moviecol/list/<int:page>',methods=["GET"])
@admin_login_req
@admin_auth
def moviecol_list(page=None):
    if page is None:
        page = 1
    page_data = MovieCol.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == MovieCol.movie_id,
        User.id == MovieCol.user_id
    ).paginate(page=page,per_page=10)
    return render_template('admin/moviecol_list.html',page_data=page_data)

"""删除收藏"""
@admin.route('/moviecol/del/<int:id>/',methods=["GET"])
@admin_login_req
@admin_auth
def moviecol_del(id=None):
    moviecol = MovieCol.query.get_or_404(id)
    db.session.delete(moviecol)
    db.session.commit()
    flash("收藏删除成功","ok")
    # 记录操作日志
    mcl=MovieCol.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == MovieCol.movie_id,
        User.id == MovieCol.user_id,
        MovieCol.id == id
    )
    oplog = OpLog(
        user_id=session["user_id"],
        ip=request.remote_addr,  # 获取登陆ip,
        reason="删除了一条收藏：%s→%s" %(mcl.user.name,mcl.movie.title)
    )
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for("admin.moviecol_list",page=1))

@admin.route('/oplog/list/<int:page>',methods=["GET"])
@admin_login_req
@admin_auth
def oplog_list(page=None):
    if page is None:
        page = 1
    page_data = OpLog.query.join(
        Admin
    ).filter(
        Admin.id == OpLog.user_id
    ).paginate(page=page, per_page=10)
    return render_template('admin/oplog_list.html',page_data=page_data)

@admin.route('/adminloginlog/list/<int:page>',methods=["GET"])
@admin_login_req
@admin_auth
def adminloginlog_list(page=None):
    if page is None:
        page = 1
    page_data = AdminLog.query.join(
        Admin
    ).filter(
        Admin.id == AdminLog.admin_id
    ).paginate(page=page, per_page=10)
    return render_template('admin/adminloginlog_list.html',page_data=page_data)

@admin.route('/userloginlog/list/<int:page>',methods=["GET"])
@admin_login_req
@admin_auth
def userloginlog_list(page=None):
    if page is None:
        page = 1
    page_data = UserLog.query.join(
        User
    ).filter(
        User.id == UserLog.user_id
    ).paginate(page=page, per_page=10)

    return render_template('admin/userloginlog_list.html',page_data=page_data)

"""添加权限"""
@admin.route('/auth/add/',methods=["GET","POST"])
@admin_login_req
@admin_auth
def auth_add():
    form = AuthForm()
    if form.validate_on_submit():
        data = form.data
        auth = Auth(
            name = data["name"],
            url = data["url"]
        )
        db.session.add(auth)
        db.session.commit()
        flash("添加权限成功","ok")
        oplog = OpLog(
            user_id=session["user_id"],
            ip=request.remote_addr,  # 获取登陆ip,
            reason="添加了权限：%s→%s→%s" % (session["admin"],data["name"],data["url"])
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for("admin.auth_add"))
    return render_template('admin/auth_add.html',form=form)

"""权限列表"""
@admin.route('/auth/list/<int:page>/',methods=["GET","POST"])
@admin_login_req
@admin_auth
def auth_list(page=None):
    if page is None:
        page = 1
    page_data = Auth.query.paginate(page=page, per_page=10)
    return render_template('admin/auth_list.html',page_data=page_data)

"""修改权限"""
@admin.route('/auth/edit/<int:id>',methods=["GET","POST"])
@admin_login_req
@admin_auth
def auth_edit(id=None):
    form = AuthForm()
    auth = Auth.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        auth_count = Auth.query.filter_by(name=data["name"]).count()
        if auth_count == 1 and auth.name != data["name"]:
            flash("权限名称已存在", "err")
            return redirect(url_for('admin.auth_edit', id=id))
        auth.name = data["name"]
        auth.url = data["url"]
        db.session.add(auth)
        db.session.commit()
        flash("修改权限成功","ok")
        oplog = OpLog(
            user_id=session["user_id"],
            ip=request.remote_addr,  # 获取登陆ip,
            reason="修改了权限：%s→%s→%s：%s→%s" % (session["admin"],auth.name,auth.url,data["name"],data["url"])
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for("admin.auth_edit",id=id))
    return render_template('admin/auth_edit.html',form=form,auth=auth)


"""权限删除"""
@admin.route('/auth/del/<int:id>/',methods=["GET"])
@admin_login_req
@admin_auth
def auth_del(id=None):
    auth = Auth.query.filter_by(id=id).first_or_404()
    db.session.delete(auth)
    db.session.commit()
    flash("权限删除成功","ok")
    # 记录操作日志
    oplog = OpLog(
        user_id=session["user_id"],
        ip=request.remote_addr,  # 获取登陆ip,
        reason="删除了一个权限：%s→%s" %(session["admin"],auth.name)
    )
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for("admin.auth_list",page=1))

"""添加角色"""
@admin.route('/role/add/',methods=["GET","POST"])
@admin_login_req
@admin_auth
def role_add():
    form = RoleForm()
    if form.validate_on_submit():
        data = form.data
        role = Role(
            name = data["name"],
            auths = ",".join(map(lambda ah:str(ah),data["auths"]))#整形转字符串
        )
        db.session.add(role)
        db.session.commit()
        flash("添加角色成功","ok")
        # 记录操作日志
        oplog = OpLog(
            user_id=session["user_id"],
            ip=request.remote_addr,  # 获取登陆ip,
            reason="添加了一个角色：%s→%s" % (session["admin"], data["name"])
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for("admin.role_add"))
    return render_template('admin/role_add.html',form=form)

"""角色列表"""
@admin.route('/role/list/<int:page>',methods=["GET"])
@admin_login_req
@admin_auth
def role_list(page=None):
    if page is None:
        page = 1
    page_data = Role.query.paginate(page=page, per_page=10)
    return render_template('admin/role_list.html',page_data=page_data)

"""修改角色"""
@admin.route('/role/edit/<int:id>',methods=["GET","POST"])
@admin_login_req
@admin_auth
def role_edit(id=None):
    form = RoleForm()
    role = Role.query.get_or_404(id)
    if request.method == "GET":
        form.auths.data = list(map(lambda ah:int(ah),role.auths.split(",")))#字符串转整形转列表
    if form.validate_on_submit():
        data = form.data
        role_count = Role.query.filter_by(name=data["name"]).count()
        if role_count == 1 and role.name != data["name"]:
            flash("角色名称已存在", "err")
            return redirect(url_for('admin.role_edit', id=id))
        role.name = data["name"]
        role.auths = auths = ",".join(map(lambda ah:str(ah),data["auths"]))
        db.session.add(role)
        db.session.commit()
        flash("修改角色成功","ok")
        oplog = OpLog(
            user_id=session["user_id"],
            ip=request.remote_addr,  # 获取登陆ip,
            reason="修改了角色：%s→%s：%s" % (session["admin"],role.name,data["name"])
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for("admin.role_edit",id=id))
    return render_template('admin/role_edit.html',form=form,role=role)

"""删除角色"""
@admin.route('/role/del/<int:id>/',methods=["GET"])
@admin_login_req
@admin_auth
def role_del(id=None):
    role = Role.query.filter_by(id=id).first_or_404()
    db.session.delete(role)
    db.session.commit()
    flash("角色删除成功","ok")
    # 记录操作日志
    oplog = OpLog(
        user_id=session["user_id"],
        ip=request.remote_addr,  # 获取登陆ip,
        reason="删除了一个角色：%s→%s" %(session["admin"],role.name)
    )
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for("admin.role_list",page=1))

"""添加管理员"""
@admin.route('/admin/add/',methods=["GET","POST"])
@admin_login_req
@admin_auth
def admin_add():
    form = AdminForm()
    if form.validate_on_submit():
        data = form.data
        admin_count = Admin.query.filter_by(name=data["name"]).count()
        if admin_count == 1:
            flash("管理员名称已存在", "err")
            return redirect(url_for('admin.admin_add'))
        admin = Admin(
            name = data["name"],
            pwd = generate_password_hash(data["pwd"]),
            is_super = 1,
            role_id = data["role_id"]
        )
        db.session.add(admin)
        db.session.commit()
        flash("添加管理员成功", "ok")
        # 记录操作日志
        oplog = OpLog(
            user_id=session["user_id"],
            ip=request.remote_addr,  # 获取登陆ip,
            reason="添加了一个管理员：%s→%s" % (session["admin"], data["name"])
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for("admin.admin_add"))
    return render_template('admin/admin_add.html',form=form)

"""管理员列表"""
@admin.route('/admin/list/<int:page>/',methods=["GET"])
@admin_login_req
@admin_auth
def admin_list(page=None):
    if page is None:
        page = 1
    page_data = Admin.query.join(
        Role
    ).filter(
        Role.id == Admin.role_id
    ).paginate(page=page, per_page=10)
    return render_template('admin/admin_list.html',page_data=page_data)