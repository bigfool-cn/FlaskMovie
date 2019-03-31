#coding:utf8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,FileField,TextAreaField,SelectField,SelectMultipleField
from wtforms.validators import DataRequired, ValidationError,EqualTo
from flask import session

from app.models import Admin,Tag,Auth,Role
from app import create_app

app = create_app('default')
app.app_context().push()
tags = Tag.query.all()
auths_list = Auth.query.all()
roles = Role.query.all()

class LoginForm(FlaskForm):
    """管理员登陆表单"""
    account = StringField(
        label="账号",
        validators=[DataRequired("请输入账号！")],
        description="账号",
        render_kw={
            "class ": "form-control",
            "placeholder":"请输入账号！",
            #"required":"required"
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[DataRequired("请输入密码！")],
        description="密码",
        render_kw={
            "class ": "form-control",
            "placeholder": "请输入密码！",
            #"required": "required"
        }
    )
    submit = SubmitField(
        "登陆",
        render_kw={
            "class ": "btn btn-primary btn-block btn-flat",
        }
    )
    def validate_account(self,field):
        account = field.data
        admin = Admin.query.filter_by(name=account).count()
        if admin == 0:
            raise ValidationError("账号不存在")

class TagForm(FlaskForm):
    name = StringField(
        label="标签名称",
        validators = [DataRequired("请输入标签")],
        description = "标签名称",
        render_kw={
            "class":"form-control",
            "id":"input_name",
            "placeholder":"请输入标签名称！"
        }
    )
    submit = SubmitField(
        "提交",
        render_kw={
            "class ": "btn btn-primary",
        }
    )

class MovieForm(FlaskForm):
    title = StringField(
        label="片名",
        validators=[DataRequired("请输入片名")],
        description="片名",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入片名！"
        }
    )
    url = FileField(
        label="文件",
        validators=[DataRequired("请上传")],
        description="文件",
    )
    info = TextAreaField(
        label="简介",
        validators=[DataRequired("请输入简介")],
        description="简介",
        render_kw={
            "class": "form-control",
            "row": 10
        }
    )
    logo = FileField(
        label="封面",
        validators=[DataRequired("请选择封面")],
        description="封面",
    )
    star = SelectField(
        label="星级",
        validators=[DataRequired("请选择星级")],
        description="星级",
        coerce=int,
        choices=[(1,"1星"),(2,"2星"),(3,"3星"),(4,"4星"),(5,"5星")],
        render_kw={
            "class": "form-control",
            "id":"input_star"
        }
    )
    tag_id = SelectField(
        label="标签",
        validators=[DataRequired("请选择标签")],
        description="标签",
        coerce=int,
        choices=[(v.id,v.name) for v in tags ],
        render_kw={
            "class": "form-control",
            "id":"input_tag_id"
        }
    )
    area = StringField(
        label="地区",
        validators=[DataRequired("请输入地区")],
        description="地区",
        render_kw={
            "class": "form-control",
            "id":"input_area",
            "placeholder": "请输入地区！"
        }
    )
    length = StringField(
        label="片长",
        validators=[DataRequired("请输入片长")],
        description="片长",
        render_kw={
            "class": "form-control",
            "id":"input_length",
            "placeholder": "请输入片长！"
        }
    )
    release_time = StringField(
        label="上映时间",
        validators=[DataRequired("请选择上映时间")],
        description="上映时间",
        render_kw={
            "class": "form-control",
            "id":"input_release_time",
            "placeholder": "请输入片长！"
        }
    )
    submit = SubmitField(
        "提交",
        render_kw={
            "class ": "btn btn-primary",
        }
    )

class PreviewForm(FlaskForm):
    title = StringField(
        label="预告标题",
        validators=[DataRequired("请输入预告标题")],
        description="预告标题",
        render_kw={
            "class": "form-control",
            "id": "input_title",
            "placeholder": "请输入预告标题！"
        }
    )
    logo = FileField(
        label="预告封面",
        validators=[DataRequired("请选择预告封面")],
        description="预告封面",
        render_kw={
            "id": "input_logo",
        }
    )
    submit = SubmitField(
        "提交",
        render_kw={
            "class ": "btn btn-primary",
        }
    )

class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label="旧密码",
        validators=[DataRequired("请输入旧密码！")],
        description="旧密码",
        render_kw={
            "class ": "form-control",
            "id":"input_oldpwd",
            "placeholder": "请输入旧密码！",
        }
    )
    new_pwd = PasswordField(
        label="新密码",
        validators=[DataRequired("请输入新密码！"),EqualTo('new_pwd2',message='新密码不一致')],
        description="新密码",
        render_kw={
            "class ": "form-control",
            "id":"input_newpwd",
            "placeholder": "请输入新密码！",
        }
    )
    new_pwd2 = PasswordField(
        label="确认新密码",
        validators=[DataRequired()],
        description="确认新密码",
        render_kw={
            "class ": "form-control",
            "placeholder": "请输入新密码！"
        }
    )
    submit = SubmitField(
        "提交",
        render_kw={
            "class ": "btn btn-primary",
        }
    )

    """验证旧密码"""
    def validate_old_pwd(self,filed):
        pwd = filed.data
        name = session["admin"]
        admin = Admin.query.filter_by(name=name).first()
        if not admin.check_pwd(pwd):
            raise ValidationError("旧密码输入错误")

class AuthForm(FlaskForm):
    name = StringField(
        label="权限名称",
        validators=[DataRequired("请输入权限名称")],
        description="权限名称",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入权限名称！"
        }
    )
    url = StringField(
        label="权限地址",
        validators=[DataRequired("请输入权限地址")],
        description="权限地址",
        render_kw={
            "class": "form-control",
            "id": "input_url",
            "placeholder": "请输入权限地址！"
        }
    )
    submit = SubmitField(
        "提交",
        render_kw={
            "class ": "btn btn-primary",
        }
    )

class RoleForm(FlaskForm):
    name = StringField(
        label="角色名称",
        validators=[DataRequired("请输入角色名称")],
        description="角色名称",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入角色名称！"
        }
    )
    auths = SelectMultipleField(
        label="操作权限",
        validators=[DataRequired("请选择权限列表")],
        description="操作权限",
        coerce=int,
        choices=[(a.id,a.name) for a in auths_list],
        render_kw={
            "class": "form-control",
            "id": "input_url",
            "placeholder": "请选择权限列表！"
        }
    )
    submit = SubmitField(
        "提交",
        render_kw={
            "class ": "btn btn-primary",
        }
    )

class AdminForm(FlaskForm):
    """管理员添加表单"""
    name = StringField(
        label="管理员名称",
        validators=[DataRequired("请输入管理员名称！")],
        description="管理员名称",
        render_kw={
            "class ": "form-control",
            "id":"input_name",
            "placeholder":"请输入管理员名称！",
        }
    )
    pwd = PasswordField(
        label="管理员密码",
        validators=[DataRequired("请输入管理员密码！")],
        description="管理员密码",
        render_kw={
            "class ": "form-control",
            "id": "input_pwd",
            "placeholder": "请输入密码！",
        }
    )
    re_pwd = PasswordField(
        label="管理员重复密码",
        validators=[DataRequired("请输入管理员密码！"),EqualTo("pwd",message="两次输入密码不一致")],
        description="管理员重复密码",
        render_kw={
            "class ": "form-control",
            "id": "input_re_pwd",
            "placeholder": "请再次输入管理员密码！"
        }
    )
    role_id = SelectField(
        label = "所属角色",
        validators=[DataRequired("请选择角色")],
        coerce=int,
        choices=[(r.id,r.name) for r in roles],
        render_kw={
            "class ": "form-control",
            "id": "input_role_id",
        }
    )
    submit = SubmitField(
        "提交",
        render_kw={
            "class ": "btn btn-primary",
        }
    )
