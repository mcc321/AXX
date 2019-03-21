from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import  Required,Email
from flask_wtf import FlaskForm
from flask_login import UserMixin , current_user , AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app,jsonify
import datetime
from . import db , login_manager
import bleach
from markdown import markdown
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash


#Login_manager回调函数
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


#处理未登录情况
@login_manager.unauthorized_handler
def unauthorized_handler():
    return jsonify({
        "statusCode":404
    })


#表单类
class Login_Form(FlaskForm):
    username=StringField('username',validators=[Required()])
    password=PasswordField('password',validators=[Required()])
    submit=SubmitField('Login')
    def mcc_validate(self):
        if self.username.data and self.password.data:
            return True
        else:
            return False


class Register_Form(FlaskForm):
    username=StringField('username',validators=[Required()])
    password=PasswordField('password',validators=[Required()])
    email=StringField('email',validators=[Required()])
    submit=SubmitField('submit')
    def mcc_validate(self):
        if self.username.data and self.password.data and self.email.data:
            return True
        else:
            return False




class CommentForm(FlaskForm):
    body = StringField('Enter your comment', validators=[Required()])
    submit = SubmitField('Submit')
    def mcc_validate(self):
        if self.body:
            return True
        else:
            return False

user_search=db.Table('user_search',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('search_id', db.Integer, db.ForeignKey('search_information.id')))


class User(UserMixin,db.Model):
    __tablename__ = 'user'
    __table_args__ = {'mysql_charset': 'utf8'}
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(30),unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(30),unique=True)
    icon = db.Column(db.String(200),default="https://github.com/mcc321/mcc/blob/master/img/9.jpg?raw=true")
    confirmed = db.Column(db.Boolean,default=False)

    search_information = db.relationship('Search_information', backref = 'user', lazy='dynamic',cascade='save-update,delete,merge',secondary=user_search)
    comment = db.relationship('Comment',backref = 'user', lazy='dynamic',cascade='save-update,delete,merge')
    message = db.relationship('Message',backref = 'user', lazy='dynamic',cascade='save-update,delete,merge')
    course = db.relationship('Course',backref = 'user', lazy='dynamic',cascade='save-update,delete,merge')
    role_id = db.Column(db.Integer , db.ForeignKey('role.id'))

    def __init__(self,**kwargs):
        super().__init__()
        if 'name' in kwargs:
            self.name = kwargs['name']
        if 'password' in kwargs:
            self.password = generate_password_hash(kwargs['password'])
        if 'email' in kwargs:
            self.email = kwargs['email']
        if 'icon' in kwargs:
            self.icon = kwargs['icon']
        if 'confirmed' in kwargs:
            self.confirmed = bool(kwargs['confirmed'])
        if 'search_information' in kwargs:
            tmp = Search_information.query.filter_by(search_information=kwargs['search_information']).first()
            if tmp:
                tmp.search_time += 1
                if tmp not in self.search_information:
                    self.search_information.append(tmp)
            else:
                self.search_information.append(Search_information(**kwargs))
        if 'comment_body' in kwargs and 'comment_course_id' in kwargs and 'comment_on_user_id' in kwargs:
            self.comment.append(Comment(**kwargs))
        if 'message_content' in kwargs and 'message_from_name' in kwargs:
            self.message.append(Message(**kwargs))
        if 'role' in kwargs:
            self.Role=Role.query.filter_by(role=kwargs['role'])
        if 'course_name' in kwargs and 'course_name' in kwargs and 'course_score' in kwargs and 'course_target' in kwargs \
            and 'course_address' in kwargs and 'course_class_num' in kwargs and 'course_time_start' in kwargs \
            and 'course_time_end' in kwargs and 'course_attr' in kwargs and 'course_teacher_name' in kwargs \
            and 'course_check_type' in kwargs:
            self.course.append(Course(**kwargs))
        if 'course_full' in kwargs:
            self.course.append(kwargs['course_full'])
        if 'comment_full' in kwargs:
            self.comment.append(kwargs['comment_full'])
        if 'message_full' in kwargs:
            self.message.append(kwargs['message_full'])
        if 'search_information_full' in kwargs:
            self.search_information.append(kwargs['search_information_full'])


    def generate_activate_token(self, expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id})


    @staticmethod
    def check_activate_token(self,token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        user = User.query.get(data['id'])
        if not user:
            # 用户已被删除
            return False
        # 没有激活时才需要激活
        if not user.confirmed:
            user.confirmed = True
            db.session.add(user)
            db.session.commit()
        return True
    def get_recent_search(self):
        tmp = self.search_information.all()
        tmp_len = len(tmp)
        search_information = []
        if tmp_len > 10:
            for i in tmp[-1:-10]:
                search_information.append(i.search_information)
        else:
            for i in tmp[::-1]:
                search_information=i.search_information
        return search_information

    @staticmethod
    def get(id):
        user=User.query.filter_by(id=id).first()
        return user

    def modify_password(self, password):
        self.password=generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)



class Message(db.Model):
    __tablename__ = 'message'
    __table_args__ = {'mysql_charset': 'utf8'}
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    message_content = db.Column(db.Text,nullable=False)
    message_from_name = db.Column(db.String(30),nullable=False)
    message_data = db.Column(db.DateTime,default = datetime.datetime.utcnow())
    message_user_id = db.Column(db.Integer , db.ForeignKey('user.id'))
    def __init__(self,**kwargs):
        super().__init__()
        if 'message_content' in kwargs:
            self.message_content = kwargs['message_content']
        if 'message_from_name' in kwargs:
            self.message_from_name = kwargs['message_from_name']
        if 'message_user_full' in kwargs:
            self.user = kwargs['message_user_full']
    def get_message(self):
        dic={'message_content':self.message_content ,'message_from_name':self.message_from_name ,'message_data':self.message_data}
        return dic
    def to_json(self):
        return {'message_content':self.message_content,'message_from_name':self.message_from_name}





#角色模型
class Role(db.Model):
    __tablename__='role'
    __table_args__ = {'mysql_charset': 'utf8'}
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    role = db.Column(db.String(50),unique=True)
    user = db.relationship('User',backref = 'role', lazy='dynamic')
    def __init__(self,**kwargs):
        super().__init__()
        if 'role' in kwargs:
            self.role=kwargs['role']

    @staticmethod
    def insert_roles():
        roles=["annoyance","user","admin","super_admin"]
        for r in roles:
            role = Role.query.filter_by(role=r).first()
            if role is None:
                role = Role(role=r)
            db.session.add(role)
            db.session.commit()





class Comment(db.Model):
    __tablename__ = "comment"
    __table_args__ = {'mysql_charset': 'utf8'}
    id = db.Column(db.Integer,primary_key = True,autoincrement=True)
    comment_body =  db.Column(db.Text,nullable=False)
    comment_date = db.Column(db.DateTime , index = True , default = datetime.datetime.utcnow())
    comment_on_user_id = db.Column(db.Integer,nullable=False)
    comment_course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    comment_user_id = db.Column(db.Integer , db.ForeignKey('user.id'))


    def __init__(self,**kwargs):
        super().__init__()
        if 'comment_body' in kwargs:
            self.comment_body=kwargs['comment_body']
        if 'comment_course_id' in kwargs:
            self.comment_course_id=int(kwargs['comment_course_id'])
        if 'comment_on_user_id' in kwargs:
            self.comment_on_user_id=int(kwargs['comment_on_user_id'])
        if 'comment_user_full' in kwargs:
            self.user=kwargs['comment_user_full']
        if 'comment_course_full' in kwargs:
            self.comment=kwargs['comment_course_full']
    def to_json(self):
        return {'comment_body':self.comment_body,'comment_course_id':self.comment_course_id\
                ,'comment_on_user_id':self.comment_on_user_id}

    @staticmethod
    def on_changed_body(target,value,oldvalue,initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i','strong']
        target.body_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'),
                            tags=allowed_tags, strip=True))
db.event.listen(Comment.comment_body, 'set', Comment.on_changed_body)




class Search_information(db.Model):
    __tablename__ = "search_information"
    __table_args__ = {'mysql_charset': 'utf8'}
    id = db.Column(db.Integer,primary_key = True,autoincrement=True)
    search_information = db.Column(db.String(50),nullable=False)
    search_date = db.Column(db.DateTime , index = True , default = datetime.datetime.utcnow())
    search_time = db.Column(db.Integer,default=1)

    search_user_id = db.Column(db.Integer , db.ForeignKey('user.id'))
    def __init__(self,**kwargs):
        super().__init__()
        if 'search_information' in kwargs:
            self.search_information=kwargs['search_information']
        if 'search_user_full' in kwargs:
            self.user=kwargs['search_user_full']


    @staticmethod
    def get_popular_search_information():
        tmp = Search_information.query.order_by(Search_information.search_time.desc()).all() ##反向排序
        tmp_len=len(tmp)
        search_information = []
        if tmp_len>=10:
            for i in range(10):
                search_information.append(tmp[i].search_information)
        else:
            for i in range(tmp_len):
                search_information.append(tmp[i].search_information)
        return search_information






class Course(db.Model):
    __tablename__ = "course"
    __table_args__ = {'mysql_charset': 'utf8'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_name = db.Column(db.String(20),nullable=False)
    course_type = db.Column(db.String(20),nullable=False)
    course_score = db.Column(db.Integer,nullable=False)
    course_target = db.Column(db.String(50),nullable=False)
    course_address = db.Column(db.String(50),nullable=False)
    course_class_num = db.Column(db.String(50),nullable=False)
    course_time_start = db.Column(db.Integer,nullable=False)
    course_time_end = db.Column(db.Integer,nullable=False)
    course_attr = db.Column(db.String(20),nullable=False)
    course_teacher_name = db.Column(db.String(20),nullable=False)
    course_check_type = db.Column(db.String(20),nullable=False)
    comment = db.relationship('Comment',backref = 'course', lazy='dynamic',cascade='save-update,delete,merge')
    course_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __init__(self,**kwargs):
        super().__init__()
        addr=['东九楼','西十二楼']
        targets = ['全校本科生', '硕博', '全校学生']
        course_check_types=['论文','考试']
        attrs = ['点名','签到','不点名不签到']
        course_types=['沟通与管理']
        if 'course_name' in kwargs:
            self.course_name=kwargs['course_name']
        if 'course_type' in kwargs:
            self.course_type = course_types[int(kwargs['course_type'])]
        if 'course_score' in kwargs:
            self.course_score = int(kwargs['course_score'])
        if 'course_target' in kwargs:
            self.course_target = targets[int(kwargs['course_target'])]
        if 'course_address' in kwargs:
            self.course_address = addr[int(kwargs['course_address'])]
        if 'course_class_num' in kwargs:
            self.course_class_num = kwargs['course_class_num']
        if 'course_time_start' in kwargs:
            self.course_time_start = int(kwargs['course_time_start'])
        if 'course_time_end' in kwargs:
            self.course_time_end = int(kwargs['course_time_end'])
        if 'course_attr' in kwargs:
            self.course_attr = attrs[int(kwargs['course_attr'])]
        if 'course_teacher_name' in kwargs:
            self.course_teacher_name=kwargs['course_teacher_name']
        if 'course_check_type' in kwargs:
            self.course_check_type=course_check_types[int(kwargs['course_check_type'])]
        if 'course_user' in kwargs:
            self.user = kwargs['course_user']
        if 'course_comment' in kwargs:
            self.comment.append(kwargs['course_comment'])












