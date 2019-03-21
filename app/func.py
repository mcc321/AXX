from .models import User ,Comment,Message,Course,Search_information,Role
from . import db,login_manager
from flask import request , render_template , flash , jsonify , current_app
import json , re , time , datetime
from flask_mail import Message
import datetime
from sqlalchemy.exc import SQLAlchemyError
from flask_login import current_user
from werkzeug.security import generate_password_hash
from flask_jwt import JWT, jwt_required, current_identity



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
    if current_user.is_authenticated:
        user = current_user._get_current_object()
    if current_identity:
        user = User.query.filter_by(id=current_identity.id).first()
    else:
        user=User(**kwargs)
    if 'name' in kwargs:
        user.name=kwargs['name']
    if 'password' in kwargs:
        user.password=generate_password_hash(kwargs['password'])
    if 'confirmed' in kwargs:
        user.confirmed = bool(kwargs['confirmed'])
    if 'email' in kwargs:
        user.email = kwargs['email']
    if 'icon' in kwargs:
        user.icon=kwargs['icon']
    if 'search_information' in kwargs:
        tmp=Search_information.query.filter_by(search_information=kwargs['search_information']).first()
        if tmp:
            tmp.search_time+=1
            if tmp not in user.search_information:
                user.search_information.append(Search_information(**kwargs))
        else:
            user.search_information.append(Search_information(**kwargs))
    if 'comment_body' in kwargs and 'comment_course_id' in kwargs and 'comment_on_user_id' in kwargs:
        user.comment.append(Comment(**kwargs))
    if 'message_content' in kwargs and 'message_from_user_name' in kwargs:
        user.message.append(Message(message_content=kwargs['message_content'],message_from_name=kwargs['message_from_name']))
    if 'role' in kwargs:
        user.Role = Role.query.filter_by(role=kwargs['role']).first()
    if 'course_name' in kwargs and 'course_name' in kwargs and 'course_score' in kwargs and 'course_target' in kwargs \
            and 'course_address' in kwargs and 'course_class_num' in kwargs and 'course_time_start' in kwargs \
            and 'course_time_end' in kwargs and 'course_attr' in kwargs and 'course_teacher_name' in kwargs \
            and 'course_check_type' in kwargs and 'course_time_week' in kwargs:
        user.course.append(Course(**kwargs))
    db.session.add(user)
    db.session.commit()
    return user




def db_user_push_tmp(**kwargs):
    if 'name' in kwargs:
        user = User.query.filter_by(name=kwargs['name']).first()
        if user:
            if 'name' in kwargs:
                user.name = kwargs['name']
            if 'password' in kwargs:
                user.password = generate_password_hash(kwargs['password'])
            if 'confirmed' in kwargs:
                user.confirmed = bool(kwargs['confirmed'])
            if 'email' in kwargs:
                user.email = kwargs['email']
            if 'icon' in kwargs:
                user.icon = kwargs['icon']
            if 'search_information' in kwargs:
                tmp = Search_information.query.filter_by(search_information=kwargs['search_information']).first()
                if tmp:
                    tmp.search_time += 1
                    if tmp not in user.search_information:
                        user.search_information.append(Search_information(**kwargs))
                else:
                    user.search_information.append(Search_information(**kwargs))
            if 'comment_body' in kwargs and 'comment_course_id' in kwargs and 'comment_on_user_id' in kwargs:
                user.comment.append(Comment(**kwargs))
            if 'message_content' in kwargs and 'message_from_user_name' in kwargs:
                user.message.append(
                    Message(message_content=kwargs['message_content'], message_from_name=kwargs['message_from_name']))
            if 'role' in kwargs:
                user.Role = Role.query.filter_by(role=kwargs['role']).first()
            if 'course_name' in kwargs and 'course_name' in kwargs and 'course_score' in kwargs and 'course_target' in kwargs \
                    and 'course_address' in kwargs and 'course_class_num' in kwargs and 'course_time_start' in kwargs \
                    and 'course_time_end' in kwargs and 'course_attr' in kwargs and 'course_teacher_name' in kwargs \
                    and 'course_check_type' in kwargs and 'course_time_week' in kwargs:
                user.course.append(Course(**kwargs))
        else:
            user=User(**kwargs)
        db.session.add(user)
        db.session.commit()
        return user
    else:
        return None





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
    course_check_types = ['论文', '考试','其它']
    attrs = ['点名', '签到', '不点名不签到']
    course_types = ['文学与艺术', '沟通与管理']
    course_times_week = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    if 'course_name' in kwargs:
        course=Course.query.filter_by(course_name=kwargs['course_name']).first()
        if course is None:
            course = Course(**kwargs)
        else:
            if 'course_name' in kwargs:
                course.course_name=kwargs['course_name']
            if 'course_type' in kwargs:
                course.course_type = course_types[int(kwargs['course_type'])]
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
                course.course_attr = attrs[int(kwargs['course_attr'])]
            if 'course_check_type' in kwargs:
                course.course_check_type = course_check_types[int(kwargs['course_check_type'])]
            if 'course_time_week' in kwargs:
                course.course_time_week = course_times_week[int(kwargs['course_time_week']) - 1]
        db.session.add(course)
        session_commit()
    else:
        return None
#----------------------------------------------------------------
#使用函数类，自定义的函数放这里，尽量通俗易懂，尽量简单
#----------------------------------------------------------------
def json_loads():
    fields = [k for k in request.values]
    values = [request.values[k] for k in request.values]
    data = dict(zip(fields, values))
    if 'comment_course_id' in data:
        data['comment_course_id']=int(data['comment_course_id'])
    if 'comment_on_user_id' in data:
        data['comment_on_user_id'] = int(data['comment_on_user_id'])
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
    if 'course_type' in data:
        data['course_type'] = int(data['course_type'])
    if 'course_check_type' in data:
        data['course_check_type'] = int(data['course_check_type'])
    if 'course_time_week' in data:
        data['course_time_week']=int(data['course_time_week'])

    return data


#用户提交的表单分析函数
def form_analysis(form):
    if form.mcc_validate():
        if request.method=='POST':
            dic = dict()
            username=form.username.data
            password=form.password.data
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
