import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "351e501657f84d629bbfcc940abb109e"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[JS_chen]'
    FLASKY_MAIL_SENDER = '13126051483@163.com'
    FLASKY_ADMIN = 'admin'  #os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass

#开发配置
class DevelopmentConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:csj1063944784@localhost:3306/movie'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    UP_DIR=os.path.join(os.path.abspath(os.path.dirname(__file__)),"app/static/uploads/")

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig,
}