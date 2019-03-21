from . import auth
from flask import render_template , url_for, session, redirect

from ..models import User , Login_Form , Register_Form
from flask_login import current_user , login_required , login_user , logout_user , user_logged_in
from ..func import *
from .func import *


@auth.route('/')
def index():
    return render_template('index.html')


@auth.route('/<path:path>',methods=['GET','POST'])
def any_root_path(path):
    return render_template('index.html')


@auth.route('/register',methods=['POST'])
def registerId():
    if current_user.is_authenticated:
        return jsonify({"StatusCode":400,"Current_user":current_user._get_current_object().name,"info":"您已登陆"})
    else:
        if request.method=='POST':
            form=Register_Form()
            if form.mcc_validate():
                name=form.username.data
                password=form.password.data
                email=form.email.data
                if User.query.filter_by(name=name).first() is None:
                    if mail_auth(email):
                        user=User(name=name,password=password,email=email,role="user")
                        db.session.add(user)
                        db.session.commit()
                        token = user.generate_activate_token()
                        # 发送激活邮件到注册邮箱
                        send_mail(email, '账户激活', 'auth\\templates\\Life_Is_Strange_Artwork_5.jpg', token=token,username=name)
                        # 提示用户下一步操作
                        return jsonify({"StatusCode":200})
                    else:
                        return jsonify({"StatusCode":400,"info":"email is not validate"})
                else:
                    return jsonify({"StatusCode":400,"info":"user is already register"})
            else:
                return jsonify({"StatusCode":400,"info":"表单填写错误"})
        else:
            return jsonify({"StatusCode":400,"info":"请求方式必须为POST"})


@auth.route('/login',methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return jsonify({"StatusCode": 300, "info": "您目前已登陆"})
    else:
        form=Login_Form()
        dic=form_analysis(form)
        if dic != None:
            if request.method=='POST':
                username=dic['username']
                password=dic['password']
                user=User.query.filter_by(name=username).first()
                mcc_print(user)
                if user:
                    if user is not  None and user.check_password(password) and user.confirmed==True:
                        session["username"]=username
                        session["password"]=password
                        login_user(user,True)
                        session.permanent = True
                        return jsonify({"StatusCode": 200, "info": "ok"})
                    else:
                        return jsonify({"StatusCode":300,"info":"账号密码错误或邮箱未激活"})
                else:
                    return jsonify({"StatusCode":300,"info":"用户不存在"})
            else:
                return jsonify({"StatusCode": 300, "info": "请求方式错误"})
        else:
            return jsonify({"StatusCode": 300, "info": "表单不完整"})


@auth.route('/logout',methods=['POST','GET'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return jsonify({"StatusCode":200,"info":"注销成功"})
    else:
        return jsonify({"StatusCode":400,"info":"您未登录，无法注销"})


@auth.route('/activate/<token>')
def activate(token):
    if token !=None:
        if User.check_activate_token(self=current_user,token=token):
            dic=dict()
            dic['info']='activate success'
            return jsonify({'StatusCode':200,'info':'注册成功'})
        else:
            dic=dict()
            dic['info']='activate fail'
            return jsonify({'StatusCode': 400, 'info': '注册失败'})
    else:
        return jsonify({'StatusCode': 400, 'info': '注册失败'})












