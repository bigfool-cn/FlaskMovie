#coding:utf8
from werkzeug.security import check_password_hash
from app import db
import datetime

#会员模型
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True) #编号
    name = db.Column(db.String(100),unique=True)    #昵称
    pwd = db.Column(db.String(100)) #密码
    email = db.Column(db.String(100),unique=True)   #邮箱
    phone = db.Column(db.String(11),unique=True)    #手机号
    info = db.Column(db.Text)   #简介
    face = db.Column(db.String(255),unique=True)    #头像
    addtime = db.Column(db.DateTime,index=True,default=datetime.datetime.now)   #注册时间
    uuid = db.Column(db.String(255),unique=True)    #唯一标识符
    userlogs = db.relationship('UserLog',backref='user') #会员日志外键关系关联
    comments = db.relationship('Comment',backref='user')    #评论外键关系关联
    moviecols = db.relationship('MovieCol',backref='user')    #电影收藏外键关系关联

    def __repr__(self):
        return "<User %s>"%self.name

    #验证密码
    def check_pwd(self,pwd):
        return check_password_hash(self.pwd,pwd)

#会员登陆日记模型
class UserLog(db.Model):
    __tablename__ = "userlog"
    id = db.Column(db.Integer,primary_key=True) #编号
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))    #所属会员
    ip = db.Column(db.String(100)) #登陆ip
    addtime = db.Column(db.DateTime,index=True,default=datetime.datetime.now)   #登陆时间

    def __repr__(self):
        return "<UserLog %s>"%self.id

#标签
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer,primary_key=True) #编号
    name = db.Column(db.String(100))    #标题
    addtime = db.Column(db.DateTime,index=True,default=datetime.datetime.now)    #添加时间
    movies = db.relationship('Movie',backref='tag') #电影外键关联
    def __repr__(self):
        return "<Tag %s>"%self.name


#电影
class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer,primary_key=True) #编号
    title = db.Column(db.String(255),unique=True)   #标题
    url = db.Column(db.String(255),unique=True) #标题
    info = db.Column(db.Text)   #简介
    logo = db.Column(db.String(255),unique=True)    #封面
    star = db.Column(db.SmallInteger)   #星级
    playnum = db.Column(db.BigInteger) #播放量
    commentnum = db.Column(db.BigInteger)   #评论量
    tag_id = db.Column(db.Integer,db.ForeignKey('tag.id'))  #所属标签
    area = db.Column(db.String(255))    #上映地区
    release_time = db.Column(db.Date)   #上映时间
    length = db.Column(db.String(100))  #播放时间
    addtime = db.Column(db.DateTime,index=True,default=datetime.datetime.now)    #添加时间
    comments = db.relationship('Comment',backref='movie')    #评论外键关系关联
    moviecols = db.relationship('MovieCol',backref='movie')    #电影收藏外键关系关联


    def __repr__(self):
        return "<Movie %s>"%self.title

#上映预告模型
class Preview(db.Model):
    __tablename__ = "preview"
    id = db.Column(db.Integer,primary_key=True) #编号
    title = db.Column(db.String(255),unique=True)   #标题
    logo = db.Column(db.String(255),unique=True)    #封面
    addtime = db.Column(db.DateTime,index=True,default=datetime.datetime.now)    #添加时间

    def __repr__(self):
        return "<Preview %s>"%self.title

#评论
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.Text)    #内容
    movie_id = db.Column(db.Integer,db.ForeignKey('movie.id'))  #所属电影
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))    #所属用户
    addtime = db.Column(db.DateTime,index=True,default=datetime.datetime.now)    #添加时间

    def __repr__(self):
        return "<Comment %s>"%self.id

#电影收藏
class MovieCol(db.Model):
    __tablename__ = "moviecol"
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  #添加时间

    def __repr__(self):
        return "<MovieCol %s>" % self.id

#权限
class Auth(db.Model):
    __tablename__ = "auth"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    url = db.Column(db.String(255)) #地址
    addtime = db.Column(db.DateTime,index=True,default=datetime.datetime.now)#添加时间

    def __repr__(self):
        return "<Auth %s>" % self.name

# 角色
class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    auths = db.Column(db.String(600))  # 权限列表
    admins = db.relationship('Admin',backref='role')   #管理员关系关联
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 添加时间

    def __repr__(self):
        return "<Role %s>" % self.name

#管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 管理员账号
    pwd = db.Column(db.String(100))  # 管理员密码
    is_super = db.Column(db.SmallInteger)   #是否是超级管理员 0为是
    role_id = db.Column(db.Integer,db.ForeignKey('role.id'))    #所属角色
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 添加时间
    adminlogs = db.relationship('AdminLog',backref='admin') #管理员操作日志关系关联
    oplogs = db.relationship('OpLog',backref='admin')   #操作日志关系关联

    def __repr__(self):
        return "<Admin %s>" % self.name

    def check_pwd(self,pwd):
        return check_password_hash(self.pwd,pwd)


#管理员登陆日志
class AdminLog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 登陆ip
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 登陆时间

    def __repr__(self):
        return "<AdminLog %s>" % self.id

#操作日志
class OpLog(db.Model):
    __tablename__ = "oplog"
    id = db.Column(db.Integer,primary_key=True) #编号
    user_id = db.Column(db.Integer,db.ForeignKey('admin.id'))    #所属会员
    ip = db.Column(db.String(100)) #登陆ip
    reason = db.Column(db.String(600))  #操作原因
    addtime = db.Column(db.DateTime,index=True,default=datetime.datetime.now)   #登陆时间

    def __repr__(self):
        return "<OpLog %s>"%self.id