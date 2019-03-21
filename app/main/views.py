from . import main
from ..func import *
from .func import *
from ..models import User , Login_Form , Register_Form ,Comment , CommentForm,Role
from flask_login import login_required , current_user
from flask import url_for,redirect,jsonify,render_template , current_app
import sys
from ..auth.func import *
from ..util.wraps import *
from flask_jwt import JWT, jwt_required, current_identity








# #-----------------------------------------------通用模块------------------------------------------------
@main.route('/',methods=['POST','GET'])
def index():
    from ..auth import auth
    return render_template('ForWindowsIndex.html')


@main.route('/<path:path>',methods=['GET','POST'])
def any_root_path(path):
    return render_template('index.html')



@main.route('/fake')
def makeFake():
    # userFake(10)
    userFake(10)
    commentFake(30)
    courseFake(10)
    return "success"






#---------------------------------------------------------------------------------
#---------------------------------------user路由----------------------------------
@main.route("/user/information",methods=['POST','GET'])
@jwt_required()
def user_information():
    dic=json_loads()
    db_user_push(**dic)
    user = User.query.filter_by(id=current_identity.id).first()
    return jsonify({'icon':user.icon,'name':user.name,'email':user.email})


@main.route("/user/search",methods=['POST','GET'])
@jwt_required()
def user_search():
    if current_identity:
        user = User.query.filter_by(id=current_identity.id).first()
        return jsonify({'StatusCode':200,"most_popular_search":Search_information.get_popular_search_information()\
                           ,'user_recent_search':user.get_recent_search()})
    else:
        return jsonify({'StatusCode': 200, "most_popular_search": Search_information.get_popular_search_information()})


@main.route("/user/messages",methods=['POST','GET'])
@jwt_required()
def user_messages():
    user = User.query.filter_by(id=current_identity.id).first()
    dic=json_loads()
    current = int(dic["current"])
    pagesize=int(dic["pagesize"])
    pagination = user.message.paginate(
                         page=current,
                         per_page=pagesize,
                         error_out=False
                     )
    messages=pagination.items
    prev = None
    if pagination.has_prev:
        prev=url_for("main.user_messages",page=current-1,_external=True)
    next = None
    if pagination.has_next:
        next=url_for("main.user_messages",page=current+1,_external=True)
    return jsonify({
                       "message":[message.to_json() for message in messages],
                       "prev":prev,
                       "next":next,
                       "total":pagination.total#记录总数
                   })

@main.route("/user/comments",methods=['POST','GET'])
@jwt_required()
def user_comments():
    user = User.query.filter_by(id=current_identity.id).first()
    dic=json_loads()
    current = int(dic["current"])
    pagesize=int(dic["pagesize"])
    pagination = user.comment.paginate(
                         page=current,
                         per_page=pagesize,
                         error_out=False
                     )
    comments=pagination.items
    prev = None
    if pagination.has_prev:
        prev=url_for("main.user_comments",page=current-1,_external=True)
    next = None
    if pagination.has_next:
        next=url_for("main.user_comments",page=current+1,_external=True)
    return jsonify({
                       "message":[comment.to_json() for comment in comments],
                       "prev":prev,
                       "next":next,
                       "total":pagination.total#记录总数
                   })



@main.route("/course/filter",methods=['POST','GET'])
@jwt_required()
def course_filter():
    addr = ['东九楼', '西十二楼']
    targets = ['全校本科生', '硕博', '全校学生']
    course_check_types = ['论文', '考试','其它']
    attrs = ['点名', '签到', '不点名不签到']
    course_types = ['沟通与管理']
    course_times_week = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    dic = json_loads()
    courses=[]
    if 'course_time_week' in dic:
        for c in Course.query.all():
            if c.course_time_week==course_times_week[int(dic['course_time_week'])]:
                courses.append(c)
    if courses:
        if 'course_type' in dic:
            for c in courses:
                if c.course_name!=course_types[int(dic['course_type'])]:
                    courses.pop(c)
    if not courses:
        if 'course_type' in dic:
            for c in Course.query.all():
                if c.course_type==course_types[int(dic['course_type'])]:
                    courses.append(c)

    if courses:
        if 'course_attr' in dic:
            for c in courses:
                if c.course_attr!=attrs[int(dic['course_attr'])]:
                    courses.pop(c)
    if not courses:
        if 'course_attr' in dic:
            for c in Course.query.all():
                if c.course_attr==attrs[int(dic['course_attr'])]:
                    courses.append(c)

    if courses:
        if 'course_check_type' in dic:
            for c in courses:
                if c.course_check_type!=course_check_types[int(dic['course_check_type'])]:
                    courses.pop(c)
    if not courses:
        if 'course_check_type' in dic:
            for c in Course.query.all():
                if c.course_check_type==course_check_types[int(dic['course_check_type'])]:
                    courses.append(c)

    if courses:
        if 'course_address' in dic:
            for c in courses:
                if c.course_address!=addr[int(dic['course_address'])]:
                    courses.pop(c)
    if not courses:
        if 'course_address' in dic:
            for c in Course.query.all():
                if c.course_address==addr[int(dic['course_address'])]:
                    courses.append(c)

    current = int(dic["current"])
    pagesize = int(dic["pagesize"])
    ids=[]
    for c in courses:
        ids.append(c.id)
    pagination = Course.query.filter(Course.id.in_(ids)).paginate(
        page=current,
        per_page=pagesize,
        error_out=False
    )
    courses2 = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for("main.user_comments", page=current - 1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for("main.user_comments", page=current + 1, _external=True)
    return jsonify({
        "course": [courses.to_json() for courses in courses2],
        "prev": prev,
        "next": next,
        "total": pagination.total  # 记录总数
    })


@main.route("/course/comment",methods=['POST','GET'])
@jwt_required()
def course_comment():
    user = User.query.filter_by(id=current_identity.id).first()
    dic = json_loads()
    if 'comment_body' in dic and 'comment_course_id' in dic:
        course = Course.query.filter_by(id=dic['comment_course_id']).first()
        c = {}
        t = 0
        for i in course.comment.order_by('-comment_date').all():
            c.update(
                {t: {'comment_user_name': i.user.name, 'comment_body': i.comment_body, 'comment_date': i.comment_date}})
            t += 1
        if 'is_comment_on_user' in dic:
            if bool(dic['is_comment_on_user']) and 'comment_on_user_id' in dic:
                user_tmp=User.query.filter_by(id=dic['comment_on_user_id']).first()
                str1 = user.name+"评论了您在"+course.course_name+"课程的评论"
                mcc_print(str1)
                message=Message()
                message.message_content=str1
                message.message_from_name=user.name
                message.user=user_tmp
                c_tmp=Comment(**dic)
                user.comment.append(c_tmp)
                c.update(
                    {t: {'comment_user_name': user.name, 'comment_body': dic['comment_body'],
                         'comment_date': c_tmp.comment_date}})
                db.session.add(user_tmp)
                db.session.commit()
            else:
                user.comment.append(Comment(**dic))
        else:
            user.comment.append(Comment(**dic))
        db.session.add(user)
        db.session.commit()
        return jsonify({'StatusCode': 200, 'info': '评论用户成功', 'comment_all': c})
    else:
        return jsonify({'StatusCode':400,'info':'请求未填写完整'})


























#-----------------------------------------------测试模块---------------------------------------------------

@main.route('/test1')
@login_required
def test1():
    user=current_user._get_current_object()
    return jsonify({"StatusCode":200,"name":user.name,"info":'测试成功'})


@main.route('/test2')
@jwt_required()
def test2():
    user=User.query.filter_by(id=current_identity.id).first()
    return jsonify({'StatusCode':200,'username':user.name,'info':'测试成功'})




