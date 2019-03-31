from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from app import create_app, db
from app.models import User, UserLog, Tag, Movie, Preview, Comment, MovieCol, Auth, Role, Admin, AdminLog, OpLog

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app,db)

def make_shell_context():
    return dict(app=app,db=db,User=User,UserLog=UserLog,Tag=Tag,Movie=Movie,Preview=Preview,Comment=Comment,MovieCol=MovieCol,Auth=Auth,Role=Role,Aadmin=Admin,AdminLog=AdminLog,OpLog=OpLog)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()