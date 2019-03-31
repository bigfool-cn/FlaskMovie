from flask import  redirect, url_for,session,request,abort
from functools import wraps
from . import admin
from app.models import Admin,Role,Auth
import uuid
import datetime
import os
"""上下应用文处理器"""
@admin.context_processor
def tpl_extra():
    data = dict(
        online_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    return data

"""登录验证装饰器"""
def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if not session.get("admin",False):
            return redirect(url_for('admin.login',next=request.url))
        return f(*args,**kwargs)
    return decorated_function

"""更改上传文件名"""
def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]#取出后缀
    return filename

"""权限控制装饰器"""
def admin_auth(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        admin = Admin.query.join(
            Role
        ).filter(
            Role.id == Admin.role_id,
            Admin.id == session["user_id"]
        ).first()
        auths = admin.role.auths
        auths = list(map(lambda v:int(v),auths.split(",")))
        auths_list = Auth.query.all()#获取所有权限
        urls = [v.url for v in auths_list for val in auths if v.id == val]#取出当前用户权限id对应的url
        rule = request.url_rule
        #if str(rule) not in urls:
            #abort(404)
        return f(*args,**kwargs)
    return decorated_function