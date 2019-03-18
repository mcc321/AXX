from .models import User ,Comment,Message,Course,Search_information,Role
from . import db,login_manager
from flask import request , render_template , flash , jsonify , current_app
import json , re , time , datetime
from flask_mail import Message
import datetime
from sqlalchemy.exc import SQLAlchemyError
from flask_login import current_user
from werkzeug.security import generate_password_hash




#----------------------------------------------------------------
#认证类函数,因为这里容易混淆，所以建议以库名加属性加auth来命名
#----------------------------------------------------------------
def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        dic = {'StatusCode': 400, 'info': reason}
        return jsonify(dic)


def db_user_auth(name,password):
    user=User.query.filter_by(name=name).first()
    if user.check_password(password):
        return True
    else:
        return False


def db_user_push(**kwargs):
    if 'name' in kwargs:
        user = User.query.filter_by(name=kwargs['name']).first()
        if user is None:
            user = User(**kwargs)
        else:
            user.name=kwargs['name']
            if 'password' in kwargs:
                user.password=generate_password_hash(kwargs['password'])
            if 'confirmed' in kwargs:
                user.confirmed = kwargs['confirmed']
            if 'email' in kwargs:
                user.email = kwargs['email']
            if 'icon' in kwargs:
                user.icon=kwargs['icon']
            if 'search_information' in kwargs:
                tmp=Search_information.query.filter_by(search_information=kwargs['search_information']).first()
                if tmp:
                    tmp.search_time+=1
                    db.session.add(tmp)
                    session_commit()
                    if tmp not in user.search_information:
                        user.search_information.append(Search_information(**kwargs))
                else:
                    user.search_information.append(Search_information(**kwargs))
            if 'comment_body' in kwargs and 'comment_course_id' in kwargs:
                user.comment.append(Comment(**kwargs))
            if 'message_content' in kwargs and 'message_from_user_name' in kwargs:
                user.message.append(Message(**kwargs))
            if 'role' in kwargs:
                user.Role = Role.query.filter_by(role=kwargs['role']).first()
        db.session.add(user)
        db.session.commit()
        return True
    else:
        return False


def db_message_delete(id):
    message = Message.query.filter_by(id == id).first()
    db.session.delete(message)
    session_commit()



#参数1：comment的id
def db_comment_delete(id):
    comment=Comment.query.filter_by(id==id).first()
    db.session.delete(comment)
    user=User.query.filter_by(comment=comment)
    user.message.append(Message(message_content="Your comment is delete by"+ current_user._get_current_object().name,message_from_user_name=current_user._get_current_object().name))
    db.session.add(user)
    session_commit()

def  db_course_push(**kwargs):
    addr = ['东九楼', '西十二楼']
    targets = ['全校本科生', '硕博', '全校学生']
    if 'course_name' in kwargs:
        course=Course.query.filter_by(course_name=kwargs['course_name']).first()
        if course is None:
            course = Course(**kwargs)
        else:
            if 'course_name' in kwargs:
                course.course_name=kwargs['course_name']
            if 'course_type' in kwargs:
                course.course_type = kwargs['course_type']
            if 'course_score' in kwargs:
                course.course_score = int(kwargs['course_score'])
            if 'course_target' in kwargs:
                course.course_target = targets[int(kwargs['course_target'])]
            if 'course_address' in kwargs:
                course.course_address = addr[int(kwargs['course_address'])]
            if 'course_class_num' in kwargs:
                course.course_class_num = kwargs['course_class_num']
            if 'course_time_start' in kwargs:
                course.course_time_start = int(kwargs['course_time_start'])
            if 'course_time_end' in kwargs:
                course.course_time_end = int(kwargs['course_time_end'])
            if 'course_attr' in kwargs:
                course.course_attr = int(kwargs['course_attr'])
        db.session.add(course)
        session_commit()
    else:
        return None
#----------------------------------------------------------------
#使用函数类，自定义的函数放这里，尽量通俗易懂，尽量简单
#----------------------------------------------------------------
# def json_loads():
#     pre_data=request.get_data().decode('utf-8')
#     dic=json.loads(pre_data)
#     return dic
def json_loads():
    fields = [k for k in request.values]
    values = [request.values[k] for k in request.values]
    data = dict(zip(fields, values))
    if 'comment_course_id' in data:
        data['comment_course_id']=int(data['comment_course_id'])
    if 'course_score' in data:
        data['course_score']=int(data['course_score'])
    if 'course_time_start' in data:
        data['course_time_start']=int(data['course_time_start'])
    if 'course_time_end' in data:
        data['course_time_end']=int(data['course_time_end'])
    if 'course_attr' in data:
        data['course_attr']=int(data['course_attr'])
    if 'course_target' in data:
        data['course_target']=int(data['course_target'])
    if 'course_address' in data:
        data['course_address'] = int(data['course_address'])
    return data


#用户提交的表单分析函数
def form_analysis(form):
    if form.mcc_validate():
        if request.method=='POST':
            dic = dict()
            username=form.username.data
            password=form.password.data
            if form.email.data:
                email=form.email.data
                dic['email'] = email
            #如有除username和password的属性，在这里添加
            dic['username']=username
            dic['password']=password
            return dic
    return None


def mcc_info(info):
    app=current_app._get_current_object()
    app.logger.info(info)
    flash(info)
    return info


def mcc_print(info):
    app=current_app._get_current_object()
    app.logger.info(info)  


def get_app_config(attrib):
    app=current_app._get_current_object()
    return app[attrib]
