#encoding: utf-8
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from python_pro import app
from exts import db
from flask_login import LoginManager
from models import User,Post,Comment

manager = Manager(app)
login_manager=LoginManager()
#use migrate to bound app and db
migrate = Migrate(app,db)

#添加迁移脚本的命令到manager中
manager.add_command('db',MigrateCommand)

if __name__ =='__main__':
    manager.run()
