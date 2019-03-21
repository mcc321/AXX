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


@main.route("/search",methods=['POST','GET'])
@jwt_required()
def search():
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









#-----------------------------------------------测试模块---------------------------------------------------

@main.route('/test1')
@login_required
def test():
    user=current_user._get_current_object()
    return jsonify({"StatusCode":200,"name":user.name,"info":'测试成功'})


@main.route('/test2')
@jwt_required()
def test2():
    user=User.query.filter_by(id=current_identity.id).first()
    return jsonify({'StatusCode':200,'username':user.name,'info':'测试成功'})




