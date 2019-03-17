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


class User(UserMixin,db.Model):
    __tablename__ = 'user'
    __table_args__ = {'mysql_charset': 'utf8'}
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(30),unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(30),unique=True)
    icon = db.Column(db.String(50),default="https://github.com/mcc321/mcc/blob/master/img/9.jpg?raw=true")
    confirmed = db.Column(db.Boolean,default=False)

    search_information = db.relationship('Search_information', backref = 'user', lazy='dynamic',cascade='save-update,delete,merge')
    comment = db.relationship('Comment',backref = 'user', lazy='dynamic',cascade='save-update,delete,merge')
    message = db.relationship('Message',backref = 'user', lazy='dynamic',cascade='save-update,delete,merge')


    role_id = db.Column(db.Integer , db.ForeignKey('role.id'))

    def __init__(self,**kwargs):
        super().__init__()
        self.name = kwargs['name']
        self.password = generate_password_hash(kwargs['name'])
        self.email = kwargs['email']
        self.icon = kwargs['icon']
        self.confirmed = kwargs['confirmed']
        if 'search_information' in kwargs:

            self.search_information.append(Search_information(**kwargs))
        if 'comment_body' in kwargs and 'comment_course_id' in kwargs:
            self.comment.append(Comment(**kwargs))
        if 'message_content' in kwargs and 'message_from_user_name' in kwargs:
            self.message.append(Message(**kwargs))
        if 'role_role' in kwargs:
            self.Role=Role.query.filter_by(role_role=kwargs['role_role'])


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
    message_content = db.Column(db.Text,nullable=True)
    message_from_user_name = db.Column(db.String(30),nullable=False)
    message_data = db.Column(db.DateTime,default = datetime.datetime.utcnow())
    message_user_id = db.Column(db.Integer , db.ForeignKey('user.id'))
    def __init__(self,**kwargs):
        self.message_content=kwargs['message_content']
        self.message_from_user_name = kwargs['message_from_user_name']
    def get_message(self):
        dic={'message_content':self.message_content ,'message_from_user_name':self.message_from_user_name ,'message_data':self.message_data}
        return dic




#角色模型
class Role(db.Model):
    __tablename__='role'
    __table_args__ = {'mysql_charset': 'utf8'}
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    role_role=db.Column(db.String(20),unique=True)
    user = db.relationship('User',backref = 'role', lazy='dynamic')
    def __init__(self,**kwargs):
        self.role_role=kwargs['role_role']

    @staticmethod
    def insert_roles():
        roles=['annoyance','user','admin','super_admin']
        for r in roles:
            role = Role.query.filter_by(role_role=r).first()
            if role is None:
                role = Role(role_role=r)
                db.session.add(role)
                try:
                    db.session.commit()
                except SQLAlchemyError as e:
                    db.session.rollback()




class Comment(db.Model):
    __tablename__ = "comment"
    __table_args__ = {'mysql_charset': 'utf8'}
    id = db.Column(db.Integer,primary_key = True,autoincrement=True)
    comment_body =  db.Column(db.Text,nullable=False)
    comment_date = db.Column(db.DateTime , index = True , default = datetime.datetime.utcnow())
    comment_course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    comment_user_id = db.Column(db.Integer , db.ForeignKey('user.id'))


    def __init__(self,**kwargs):
        self.comment_body=kwargs['comment_body']
        self.comment_course_id=kwargs['comment_course_id']

    @staticmethod
    def on_changed_body(target,value,oldvalue,initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i','strong']
        target.body_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'),
                            tags=allowed_tags, strip=True))
db.event.listen(Comment.body, 'set', Comment.on_changed_body)




class Search_information(db.Model):
    __tablename__ = "search_information"
    __table_args__ = {'mysql_charset': 'utf8'}
    id = db.Column(db.Integer,primary_key = True,autoincrement=True)
    search_information = db.Column(db.String(50),nullable=False)
    search_date = db.Column(db.DateTime , index = True , default = datetime.datetime.utcnow())
    search_time = db.Column(db.Integer,default=1)

    search_user_id = db.Column(db.Integer , db.ForeignKey('user.id'))
    def __init__(self,**kwargs):
        self.search_information=kwargs['search_information']
    def get_popular_search_information(self):
        tmp = Search_information.query.order_by(Search_information.search_time.desc()).all() ##反向排序
        search_information = []
        for i in range(10):
            search_information.append(tmp[i])
        return search_information






class Course(db.Model):
    __tablename__ = "course"
    __table_args__ = {'mysql_charset': 'utf8'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_name = db.Column(db.String(20),nullable=False)
    course_type = db.Column(db.String(20),nullable=False)
    course_score = db.Column(db.Integer,nullable=False)
    course_target = db.Column(db.String(40),nullable=False)
    course_address = db.Column(db.String(50),nullable=False)
    course_time_start = db.Column(db.Integer,nullable=False)
    course_time_end = db.Column(db.Integer,nullable=False)
    course_attr = db.Column(db.Integer,nullable=False)
    comment = db.relationship('Comment',backref = 'course', lazy='dynamic',cascade='save-update,delete,merge')

    def __init__(self,**kwargs):
        self.course_name=kwargs['course_name']
        self.course_type = kwargs['course_type']
        self.course_score = kwargs['course_score']
        self.course_target = kwargs['course_target']
        self.course_address = kwargs['course_address']
        self.course_time_start = kwargs['course_time_start']
        self.course_time_end = kwargs['course_time_end']
        self.course_attr = kwargs['course_attr']
    def get_attr(self):
        attr = []
        if self.course_attr&0x1:
            attr.append("点名")
        if self.course_attr & 0x2:
            attr.append("签到")
        return attr












