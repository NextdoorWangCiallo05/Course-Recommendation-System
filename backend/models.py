from datetime import datetime, timezone, timedelta
from flask_sqlalchemy import SQLAlchemy

CST = timezone(timedelta(hours=8))

def get_cst_now():
    return datetime.now(CST).replace(tzinfo=None)

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), nullable=True)  # 学号
    real_name = db.Column(db.String(50), nullable=True)  # 真实姓名
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin', 'student', 'superadmin', 'pending'), nullable=False, default='student')
    requested_role = db.Column(db.String(20), nullable=True)  # 注册时申请的角色
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Major(db.Model):
    __tablename__ = 'majors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)

class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    name_pinyin = db.Column(db.String(50), nullable=True)
    evaluations = db.relationship('Evaluation', backref='teacher', lazy=True)

course_major = db.Table('course_major',
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True),
    db.Column('major_id', db.Integer, db.ForeignKey('majors.id'), primary_key=True),
    db.Column('course_type_for_major', db.String(20), nullable=False, default='必修')  # 课程对于该专业的性质
)

course_teacher = db.Table('course_teacher',
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True),
    db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id'), primary_key=True)
)

course_semester = db.Table('course_semester',
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True),
    db.Column('semester', db.String(10), primary_key=True)  # 春季、秋季
)

course_course_type = db.Table('course_course_type',
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True),
    db.Column('course_type', db.String(20), primary_key=True)  # 公共课、学科必修、专业必修、专业选修、实践课等
)

course_major_semester = db.Table('course_major_semester',
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True),
    db.Column('major_id', db.Integer, db.ForeignKey('majors.id'), primary_key=True),
    db.Column('study_semester', db.String(10), primary_key=True)  # 大一上~大四下
)

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    credit = db.Column(db.Numeric(3, 1), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    course_type = db.Column(db.String(20), nullable=False, default='')  # 保留字段，兼容旧数据
    semester = db.Column(db.String(10), nullable=False, default='')  # 保留字段，兼容旧数据
    order_num = db.Column(db.Integer, default=0, nullable=False)  # 序号，用于排序
    college = db.Column(db.String(100), nullable=True)  # 开课学院
    assessment_method = db.Column(db.String(50), nullable=True)  # 考核方式
    topic_category = db.Column(db.String(200), nullable=True)  # 主题类别（通识选修/实践课专用）
    evaluations = db.relationship('Evaluation', backref='course', lazy=True)
    majors = db.relationship('Major', secondary=course_major, backref=db.backref('courses', lazy=True))
    teachers = db.relationship('Teacher', secondary=course_teacher, backref=db.backref('courses', lazy=True))

class Evaluation(db.Model):
    __tablename__ = 'evaluations'
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=get_cst_now)

class Feedback(db.Model):
    __tablename__ = 'feedbacks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=get_cst_now)
