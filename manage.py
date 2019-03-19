import os 
from app import create_app , db
from app.models import User , Comment , Role
from flask_script import Manager , Shell,Server
from flask_migrate import Migrate , MigrateCommand
from flask import render_template
from flask_cors import CORS
import logging

app = create_app()
CORS(app)
manager = Manager(app)
#数据库迁移
migrate = Migrate(app,db)
logging.getLogger('flask_cors').level = logging.DEBUG


def make_shell_context():
    return dict(app = app , db = db , User = User , Role=Role ,Comment=Comment)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)
manager.add_command("server", Server(host='127.0.0.1', port=5000))


@app.route('/')
def root_path():
    return render_template('index.html')


@app.route('/<path:path>',methods=['GET'])
def any_root_path(path):
    return render_template('index.html')


if __name__ == "__main__":
    manager.run()
