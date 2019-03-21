from .. import db
from ..models import User ,Comment,Course
from werkzeug.security import generate_password_hash
import random
#----------------------------------------------------------------------------------------------------
#测试使用
#----------------------------------------------------------------------------------------------------
#产生假用户
def userFake(count=100 , role = 'user',confirmd=True,icon='https://github.com/mcc321/mcc/blob/master/img/9.jpg?raw=true'):#默认人数100，默认权限2,通过验证
    from sqlalchemy.exc import IntegrityError
    from random import seed
    import forgery_py

    seed()
    for i in range(count):
        u=User(
            name=forgery_py.name.full_name(),
            password=generate_password_hash(forgery_py.lorem_ipsum.word()),
            email=forgery_py.internet.email_address(),
            role=role,
            confirmed=confirmd,
            icon=icon
        )
        db.session.add(u)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

#产生假文章
def courseFake(count=100):
    from random import seed,randint
    import forgery_py

    first_name = ["王", "李", "张", "刘", "赵", "蒋", "孟", "陈", "徐", "杨", "沈", "马", "高", "殷", "上官", "钟", "常"]
    second_name = ["伟", "华", "建国", "洋", "刚", "万里", "爱民", "牧", "陆", "路", "昕", "鑫", "兵", "硕", "志宏", "峰", "磊", "雷", "文",
                   "明浩", "光", "超", "军", "达"]
    seed()
    user_count=User.query.count()
    for i in range(count):
        u=User.query.offset(randint(0,user_count-1)).first()
        course=Course(
            course_name=random.choice(["创业基础","设计思维","创业素养及能力提升","逻辑幽默","幸福感的源泉","管理学概论","知我认知与生涯规划","情商训练","三维造型技术","信息安全导论","未来的能源","汽车概论","信息与检索","营养与健康","食品安全与卫生","气象漫谈","初级俄语"]),
            course_type=random.randint(0,0),
            course_score = random.choice([2,4]),
            course_target = random.choice([0,1,2]),
            course_address = random.choice([0,1]),
            course_class_num = random.choice(['A','B','C','D'])+str(random.randint(1,5))+str(random.randint(1,20)),
            course_time_start = random.randint(3,5),
            course_time_end = random.randint(10,15),
            course_attr = random.choice([0,1,2]),
            course_teacher_name = random.choice(first_name) + random.choice(second_name),
            course_check_type = random.choice([0,1]),
            course_time_week = random.randint(1,7),
            course_user=u
        )
        db.session.add(course)
        try:
            db.session.commit()
        except:
            db.session.rollback()

def commentFake(count=450):
    from random import seed,randint
    import forgery_py
    seed()
    user_count=User.query.count()
    course_count=Course.query.count()
    for i in range(count):
        u=User.query.offset(randint(0,user_count-1)).first()
        c=Course.query.offset(randint(0,course_count-1)).first()
        c=Comment(
            comment_body=forgery_py.lorem_ipsum.sentences(randint(1,2)),
            comment_on_user_id=random.randint(1,user_count),
            comment_user_full=u,
            comment_course_full=c
        )
        db.session.add(c)
        try:
            db.session.commit()
        except:
            db.session.rollback()

#----------------------------------------------------------------------------------------------------