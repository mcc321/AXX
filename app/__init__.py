# -*- coding: utf-8 -*-
from flask import Flask , render_template,jsonify
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import sys , os
from flask_login import LoginManager
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

mail=Mail()
moment=Moment()
db=SQLAlchemy()
login_manager=LoginManager()
login_manager.session_protection = 'strong'#设置验证密码强度


def authenticate(username, password):
    user = User.query.filter_by(name=username).first()
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user
    return None


def identity(payload):
    user_id = payload['identity']
    user = User.query.filter_by(id=user_id).first()
    if user:
        return user
    return None



from .func import *


def create_app():
    #蓝图注册
    from . import auth , main
    
    app = Flask(__name__)
    app.register_blueprint(main.main , url_prefix='/main')
    app.register_blueprint(auth.auth , url_prefix='/auth')
    jwt = JWT(app , authenticate , identity)




    #配置模块
    app.config.from_pyfile("config\\production.py")


    #模型初始化
    mail.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)

    

    #数据库初始化
    with app.app_context():
        db.create_all()
        from .models import Role
        Role.insert_roles()
        dic=dict()
        dic['name']='mcc'
        dic['email']='2561908792@qq.com'
        dic['icon']='https://github.com/mcc321/mcc/blob/master/img/9.jpg?raw=true'
        dic['confirmed']=True
        dic['password']="mcc"
        dic['search_information']="axx"
        dic['comment_body']='hello everyone!'
        dic['comment_course_id'] = "1"
        dic['role']='admin'
        dic['course_name']='幸福感的源泉'
        dic['course_type']='沟通与管理'
        dic['course_score']="2"
        dic['course_target']="0"
        dic['course_address']="0"
        dic['course_class_num']='B203'
        dic['course_time_start']="3"
        dic['course_time_end']="10"
        dic['course_attr']="3"
        db_course_push(**dic)
        db_user_push(**dic)
    return app













