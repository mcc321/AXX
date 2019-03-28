import datetime
#数据库配置
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:zc0602@127.0.0.1/axx'

#邮件配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = '@qq.com'
MAIL_PASSWORD = ''
FLASKY_MAIL_SENDER = 'Admin <@qq.com>'
FLASKY_MAIL_SUBJECT_PREFIX = 'mcc'

#session会话设置
SESSION_PROTECTION = 'haiduhaihfdasdjifahufwee'
SECRET_KEY = 'super-secret'
REMEMBER_COOKIE_DURATION = datetime.timedelta(hours=2)

#JWT设置
JWT_SECRET_KEY = 'mcc'
JWT_AUTH_URL_RULE = '/authenticate'
JWT_EXPIRATION_DELTA = datetime.timedelta(seconds=300)

#是否开启debug
DEBUG = True
#分页设置
FLASKY_COMMENTS_PER_PAGE=4




