#coding:utf8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,FileField,TextAreaField
from wtforms.validators import DataRequired, ValidationError,EqualTo,Email,Regexp
from app.models import User

class RegistForm(FlaskForm):
    name = StringField(
        label="昵称",
        validators=[DataRequired("请输入昵称！")],
        description="昵称",
        render_kw={
            "class ": "form-control input-lg",
            "id":"input_name",
            "placeholder": "请输入昵称！",
        }
    )
    email = StringField(
        label="邮箱",
        validators=[DataRequired("请输入邮箱！"),Email("邮箱格式不正确！")],
        description="邮箱",
        render_kw={
            "class ": "form-control input-lg",
            "id": "input_email",
            "placeholder": "请输入邮箱！",
        }
    )
    phone = StringField(
        label="手机号码",
        validators=[DataRequired("请输入手机号码！"), Regexp("1[3458]\\d{9}",message="手机号码格式不正确！")],
        description="手机号码",
        render_kw={
            "class ": "form-control input-lg",
            "id": "input_phone",
            "placeholder": "请输入手机号码！",
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[DataRequired("请输入密码！")],
        description="密码",
        render_kw={
            "class ": "form-control input-lg",
            "id": "input_password",
            "placeholder": "请输入密码！",
        }
    )
    re_pwd = PasswordField(
        label="确认密码",
        validators=[DataRequired("请再次输入密码！"),EqualTo("re_pwd",message="两次密码不一致")],
        description="确认密码",
        render_kw={
            "class ": "form-control input-lg",
            "id": "input_repassword",
            "placeholder": "请输入再次密码！",
        }
    )
    submit = SubmitField(
        "注册",
        render_kw={
            "class ": "btn btn-lg btn-success btn-block",
        }
    )
    #验证昵称
    def validate_name(self, field):
        name = field.data
        user = User.query.filter_by(name=name).count()
        if user == 1:
            raise ValidationError("昵称已存在")

    # 验证邮箱
    def validate_email(self, field):
        email = field.data
        user = User.query.filter_by(email=email).count()
        if user == 1:
            raise ValidationError("邮箱已存在")

    # 验证手机号码
    def validate_phone(self, field):
        phone = field.data
        user = User.query.filter_by(phone=phone).count()
        if user == 1:
            raise ValidationError("手机号码已存在")

class LoginForm(FlaskForm):
    name = StringField(
        label="账号",
        validators=[DataRequired("请输入账号！")],
        description="账号",
        render_kw={
            "class ": "form-control input-lg",
            "id":"input_contact",
            "placeholder": "请输入账号！",
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[DataRequired("请输入密码！")],
        description="密码",
        render_kw={
            "class ": "form-control input-lg",
            "id": "input_password",
            "placeholder": "请输入密码！",
        }
    )
    submit = SubmitField(
        "登陆",
        render_kw={
            "class ": "btn btn-lg btn-success btn-block",
        }
    )

    def validate_name(self, field):
        name = field.data
        user= User.query.filter_by(name=name).count()
        if user == 0:
            raise ValidationError("账号不存在")

class UserDetailForm(FlaskForm):
    name = StringField(
        label="昵称",
        validators=[DataRequired("请输入昵称！")],
        description="昵称",
        render_kw={
            "class ": "form-control input-lg",
            "id": "input_name",
            "placeholder": "请输入昵称！",
        }
    )
    email = StringField(
        label="邮箱",
        validators=[DataRequired("请输入邮箱！"), Email("邮箱格式不正确！")],
        description="邮箱",
        render_kw={
            "class ": "form-control input-lg",
            "id": "input_email",
            "placeholder": "请输入邮箱！",
        }
    )
    phone = StringField(
        label="手机号码",
        validators=[DataRequired("请输入手机号码！"), Regexp("1[3458]\\d{9}", message="手机号码格式不正确！")],
        description="手机号码",
        render_kw={
            "class ": "form-control input-lg",
            "id": "input_phone",
            "placeholder": "请输入手机号码！",
        }
    )
    face = FileField(
        label="头像",
        validators=[DataRequired("请选择头像")],
        description="头像",
    )
    info = TextAreaField(
        label="简介",
        validators=[DataRequired("请输入简介")],
        description="简介",
        render_kw={
            "class": "form-control",
            "id": "input_info",
            "row": 10
        }
    )
    submit = SubmitField(
        "保存修改",
        render_kw={
            "class ": "btn btn-success",
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
    pwd = PasswordField(
        label="新密码",
        validators=[DataRequired("请输入新密码！")],
        description="新密码",
        render_kw={
            "class ": "form-control",
            "id":"input_newpwd",
            "placeholder": "请输入新密码！",
        }
    )
    re_pwd = PasswordField(
        label="确认新密码",
        validators=[DataRequired(),EqualTo('pwd',message='两次密码不一致')],
        description="确认新密码",
        render_kw={
            "class ": "form-control",
            "placeholder": "请输入新密码！"
        }
    )
    submit = SubmitField(
        "修改密码",
        render_kw={
            "class ": "btn btn-success",
        }
    )

class CommentForm(FlaskForm):
    content = TextAreaField(
        label="内容",
        validators=[DataRequired("请输入内容！")],
        description="内容",
        render_kw={
            "id":"input_content",
            "placeholder": "请输入内容！"
        }
    )
    submit = SubmitField(
        "提交评论",
        render_kw={
            "class":"btn btn-success",
            "id":"btn-sub"
        }
    )