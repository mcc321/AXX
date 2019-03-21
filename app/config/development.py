#数据库配置
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:zhangchao0602@130.211.245.227/axx'

#邮件配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = '2561908792@qq.com'
MAIL_PASSWORD = 'cvrdbidruakuecce'
FLASKY_MAIL_SENDER = 'Admin <2561908792@qq.com>'
FLASKY_MAIL_SUBJECT_PREFIX = 'mcc'

#session会话设置
SESSION_PROTECTION = 'haiduhaihfdasdjifahufwee'
SECRET_KEY = 'super-secret'

#JWT设置
JWT_SECRET_KEY = 'mcc'
JWT_AUTH_URL_RULE = '/authenticate'
JWT_EXPIRATION_DELTA = 300

#是否开启debug
DEBUG = True
#分页设置
FLASKY_COMMENTS_PER_PAGE=4
