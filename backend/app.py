from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, User, Major, Teacher, Course, Evaluation, Feedback, course_major, course_teacher, course_semester, course_course_type, course_major_semester
from cache import cache
from datetime import datetime, timezone, timedelta
import os
from sqlalchemy import inspect
from pypinyin import lazy_pinyin

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db.init_app(app)
jwt = JWTManager(app)
cache.init_app(app)

# 东八区时区
CST = timezone(timedelta(hours=8))

def get_cst_now():
    """获取东八区当前时间"""
    return datetime.now(CST).replace(tzinfo=None)

def invalidate_course_cache():
    """清除课程相关缓存"""
    cache.delete_pattern('courses:*')

def invalidate_teacher_cache():
    """清除教师相关缓存"""
    cache.delete_pattern('teachers:*')

def invalidate_major_cache():
    """清除专业相关缓存"""
    cache.delete_pattern('majors:*')

def mask_student_id(student_id):
    """学号脱敏：保留前3位和后2位，中间用*代替"""
    if not student_id:
        return ''
    if len(student_id) <= 5:
        return student_id[:2] + '*' * (len(student_id) - 2)
    return student_id[:3] + '*' * (len(student_id) - 5) + student_id[-2:]

def mask_real_name(real_name):
    """姓名脱敏：保留姓氏，名字用*代替"""
    if not real_name:
        return ''
    if len(real_name) <= 1:
        return real_name
    return real_name[0] + '*' * (len(real_name) - 1)

def get_name_pinyin(name):
    """获取中文姓名的拼音首字母缩写"""
    if not name:
        return ''
    return ''.join([p[0] for p in lazy_pinyin(name)])

def init_db():
    with app.app_context():
        # 检查数据库是否已存在
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        # 如果数据库中没有表，才进行初始化
        if len(tables) == 0:
            print('数据库为空，正在初始化...')
            db.create_all()
            db.session.commit()
            
            # 初始化用户
            users = [
                User(username='admin', password=generate_password_hash('admin123'), role='admin'),
                User(username='student', password=generate_password_hash('student123'), role='student')
            ]
            db.session.add_all(users)
            db.session.flush()
            
            # 初始化基本专业
            majors = [
                Major(name='公共课', description='全校公共基础课程'),
                Major(name='计算机', description='计算机科学与技术专业课程'),
                Major(name='软件', description='软件工程专业课程'),
                Major(name='大数据', description='大数据技术专业课程'),
                Major(name='人工智能', description='人工智能专业课程')
            ]
            db.session.add_all(majors)
            db.session.commit()
            print('数据库初始化完成！（包含用户和基本专业）')
        else:
            print('数据库已存在，跳过初始化')
            # 确保表结构是最新的（只创建不存在的表）
            db.create_all()
            db.session.commit()
            
            # 确保超级管理员账户存在
            superadmin = User.query.filter_by(username='superadmin').first()
            if not superadmin:
                superadmin = User(username='superadmin', password=generate_password_hash('superadmin123'), role='superadmin')
                db.session.add(superadmin)
                db.session.commit()
                print('超级管理员账户已创建：superadmin / superadmin123')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and (check_password_hash(user.password, data['password']) or user.password == data['password']):
        if user.role == 'pending':
            return jsonify({'msg': '账户正在审核中，请耐心等待'}), 403
        access_token = create_access_token(identity=user.username, additional_claims={'role': user.role, 'user_id': user.id})
        return jsonify(access_token=access_token, role=user.role, username=user.username, user_id=user.id), 200
    return jsonify({'msg': '用户名或密码错误'}), 401

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data.get('username') or not data.get('password') or not data.get('role'):
        return jsonify({'msg': '请填写完整信息'}), 400
    if not data.get('real_name') or not data.get('student_id'):
        return jsonify({'msg': '请填写真实姓名和学号'}), 400
    if data['role'] not in ['admin', 'student']:
        return jsonify({'msg': '角色只能是管理员或学生'}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'msg': '用户名已存在'}), 400
    user = User(
        username=data['username'],
        password=generate_password_hash(data['password']),
        role='pending',
        requested_role=data['role'],
        real_name=data['real_name'],
        student_id=data['student_id']
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': '注册成功，等待超级管理员审核'}), 200

@app.route('/api/users', methods=['GET'])
@jwt_required()
def get_users():
    claims = get_jwt()
    if claims['role'] != 'superadmin':
        return jsonify({'msg': '权限不足'}), 403
    decrypt = request.args.get('decrypt', 'false') == 'true'
    users = User.query.all()
    return jsonify([{
        'id': u.id,
        'student_id': u.student_id if decrypt else mask_student_id(u.student_id),
        'real_name': u.real_name if decrypt else mask_real_name(u.real_name),
        'username': u.username,
        'role': u.role,
        'requested_role': getattr(u, 'requested_role', None),
        'created_at': u.created_at.strftime('%Y-%m-%d %H:%M:%S') if u.created_at else None
    } for u in users])

@app.route('/api/users', methods=['POST'])
@jwt_required()
def create_user():
    claims = get_jwt()
    if claims['role'] != 'superadmin':
        return jsonify({'msg': '权限不足'}), 403
    data = request.get_json()
    if not data.get('username') or not data.get('password') or not data.get('role'):
        return jsonify({'msg': '请填写完整信息'}), 400
    if data['role'] not in ['admin', 'student']:
        return jsonify({'msg': '角色只能是管理员或学生'}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'msg': '用户名已存在'}), 400
    user = User(
        student_id=data.get('student_id', ''),
        real_name=data.get('real_name', ''),
        username=data['username'],
        password=generate_password_hash(data['password']),
        role=data['role']
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': '账户创建成功', 'id': user.id}), 200

@app.route('/api/users/<int:user_id>/approve', methods=['PUT'])
@jwt_required()
def approve_user(user_id):
    claims = get_jwt()
    if claims['role'] != 'superadmin':
        return jsonify({'msg': '权限不足'}), 403
    target_user = User.query.get(user_id)
    if not target_user:
        return jsonify({'msg': '用户不存在'}), 404
    if target_user.role == 'superadmin':
        return jsonify({'msg': '不能修改超级管理员'}), 400
    data = request.get_json()
    action = data.get('action')
    if action == 'approve':
        target_user.role = data.get('role', target_user.requested_role or 'student')
        target_user.requested_role = None
        db.session.commit()
        return jsonify({'msg': '审核通过'}), 200
    elif action == 'reject':
        db.session.delete(target_user)
        db.session.commit()
        return jsonify({'msg': '已拒绝注册'}), 200
    return jsonify({'msg': '无效操作'}), 400

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    claims = get_jwt()
    if claims['role'] != 'superadmin':
        return jsonify({'msg': '权限不足'}), 403
    target_user = User.query.get(user_id)
    if not target_user:
        return jsonify({'msg': '用户不存在'}), 404
    if target_user.role == 'superadmin':
        return jsonify({'msg': '不能删除超级管理员'}), 400
    current_username = get_jwt_identity()
    if target_user.username == current_username:
        return jsonify({'msg': '不能删除自己'}), 400
    db.session.delete(target_user)
    db.session.commit()
    return jsonify({'msg': '账户已注销'}), 200

@app.route('/api/users/<int:user_id>/role', methods=['PUT'])
@jwt_required()
def update_user_role(user_id):
    claims = get_jwt()
    if claims['role'] != 'superadmin':
        return jsonify({'msg': '权限不足'}), 403
    target_user = User.query.get(user_id)
    if not target_user:
        return jsonify({'msg': '用户不存在'}), 404
    if target_user.role == 'superadmin':
        return jsonify({'msg': '不能修改超级管理员'}), 400
    data = request.get_json()
    new_role = data.get('role')
    if new_role not in ['admin', 'student', 'superadmin']:
        return jsonify({'msg': '无效的角色'}), 400
    if new_role == 'superadmin':
        return jsonify({'msg': '超级管理员唯一，不能更改'}), 400
    target_user.role = new_role
    db.session.commit()
    return jsonify({'msg': '角色已更新'}), 200

@app.route('/api/majors', methods=['GET'])
@jwt_required()
def get_majors():
    # 尝试从缓存获取
    cached = cache.get('majors:list')
    if cached is not None:
        return jsonify(cached)
    
    majors = Major.query.all()
    result = [{'id': m.id, 'name': m.name, 'description': m.description} for m in majors]
    
    # 存入缓存（1小时）
    cache.set('majors:list', result, timeout=app.config.get('CACHE_MAJORS_TIMEOUT', 3600))
    
    return jsonify(result)

@app.route('/api/courses', methods=['GET'])
@jwt_required()
def get_courses():
    major_id = request.args.get('major_id')
    sort_order = request.args.get('sort', 'asc')  # 排序方式：asc升序，desc降序
    course_type_filter = request.args.get('course_type')  # 课程性质筛选（支持多选，逗号分隔）
    major_course_type_filter = request.args.get('major_course_type')  # 针对专业的必修/选修筛选
    
    # 生成缓存键（包含所有查询参数）
    cache_key = f"courses:list:major={major_id}:sort={sort_order}:ct={course_type_filter}:mct={major_course_type_filter}"
    
    # 尝试从缓存获取
    cached = cache.get(cache_key)
    if cached is not None:
        return jsonify(cached)
    
    query = Course.query
    if major_id:
        try:
            query = query.filter(Course.majors.any(id=int(major_id)))
        except ValueError:
            return jsonify({'msg': '无效的专业ID'}), 400
    
    # 先获取所有课程
    if sort_order == 'desc':
        all_courses = query.order_by(Course.order_num.desc()).all()
    else:
        all_courses = query.order_by(Course.order_num.asc()).all()
    
    # 解析课程性质筛选（支持多选）
    course_types = []
    if course_type_filter:
        course_types = [ct.strip() for ct in course_type_filter.split(',') if ct.strip()]
    
    # 应用筛选
    filtered_courses = []
    for course in all_courses:
        # 获取课程的所有课程性质
        course_course_types = []
        try:
            ct_results = db.session.execute(
                course_course_type.select().where(course_course_type.c.course_id == course.id)
            ).fetchall()
            for ct in ct_results:
                course_course_types.append(ct.course_type)
        except:
            pass
        
        # 如果course_course_type表没有数据，尝试用旧的course_type字段
        if not course_course_types and hasattr(course, 'course_type') and course.course_type:
            course_course_types = [course.course_type]
        
        # 全局课程性质筛选（支持多选）
        if course_types:
            # 检查是否有交集
            has_match = False
            for ct in course_types:
                if ct in course_course_types:
                    has_match = True
                    break
            if not has_match:
                continue
        
        # 针对专业的必修/选修筛选
        if major_id and major_course_type_filter:
            # 获取该课程对该专业的课程性质
            from models import course_major
            result = db.session.execute(
                course_major.select().where(
                    course_major.c.course_id == course.id,
                    course_major.c.major_id == int(major_id)
                )
            ).fetchone()
            if not result or result.course_type_for_major != major_course_type_filter:
                continue
        
        filtered_courses.append((course, course_course_types))
    
    courses = [item[0] for item in filtered_courses]
    course_course_types_map = {item[0].id: item[1] for item in filtered_courses}
    result = []
    for course in courses:
        # 按老师分组计算评分
        teacher_ratings = {}
        evaluations = Evaluation.query.filter_by(course_id=course.id).all()
        for eval in evaluations:
            teacher_id = eval.teacher_id
            if teacher_id not in teacher_ratings:
                teacher_ratings[teacher_id] = []
            teacher_ratings[teacher_id].append(eval.rating)
        
        # 计算每个老师的平均评分
        teacher_avg_ratings = {}
        for teacher_id, ratings in teacher_ratings.items():
            teacher_avg_ratings[teacher_id] = round(sum(ratings) / len(ratings), 1)
        
        # 计算课程的整体平均评分（可选）
        all_ratings = [r for ratings in teacher_ratings.values() for r in ratings]
        avg_rating = sum(all_ratings) / len(all_ratings) if all_ratings else None
        
        # 获取每个专业的课程性质和修读学期
        major_course_types = {}
        major_study_semesters = {}
        
        # 先处理课程关联的专业
        for major in course.majors:
            # 查询course_major表获取该专业的课程性质
            from models import course_major
            course_major_result = db.session.execute(
                course_major.select().where(
                    course_major.c.course_id == course.id,
                    course_major.c.major_id == major.id
                )
            ).fetchone()
            if course_major_result:
                major_course_types[major.id] = course_major_result.course_type_for_major
            else:
                major_course_types[major.id] = '必修'  # 默认值
            
            # 查询course_major_semester表获取该专业的修读学期
            from models import course_major_semester
            try:
                cms_results = db.session.execute(
                    course_major_semester.select().where(
                        course_major_semester.c.course_id == course.id,
                        course_major_semester.c.major_id == major.id
                    )
                ).fetchall()
                major_study_semesters[major.id] = [r.study_semester for r in cms_results]
            except:
                major_study_semesters[major.id] = []
        
        # 额外查询所有主要专业的修读学期，确保学科必修课程能获取到对应专业的修读学期
        main_major_ids = [1, 2, 3, 4, 5, 6, 7, 8]
        for major_id in main_major_ids:
            # 无论课程是否与该专业关联，都查询修读学期数据
            try:
                cms_results = db.session.execute(
                    course_major_semester.select().where(
                        course_major_semester.c.course_id == course.id,
                        course_major_semester.c.major_id == major_id
                    )
                ).fetchall()
                if cms_results:
                    major_study_semesters[major_id] = [r.study_semester for r in cms_results]
            except:
                pass
        
        # 额外查询公共课专业的修读学期，确保所有课程都能获取到公共课的修读学期
        from models import course_major_semester
        # 查询专业ID为1的公共课
        try:
            cms_results = db.session.execute(
                course_major_semester.select().where(
                    course_major_semester.c.course_id == course.id,
                    course_major_semester.c.major_id == 1  # 公共课专业ID
                )
            ).fetchall()
            if cms_results:
                major_study_semesters[1] = [r.study_semester for r in cms_results]
        except:
            pass
        # 查询专业ID为7的公共课（备用）
        try:
            cms_results = db.session.execute(
                course_major_semester.select().where(
                    course_major_semester.c.course_id == course.id,
                    course_major_semester.c.major_id == 7  # 公共课专业ID
                )
            ).fetchall()
            if cms_results:
                major_study_semesters[7] = [r.study_semester for r in cms_results]
        except:
            pass

        # 获取课程的所有学期（带异常处理）
        semesters = []
        try:
            semester_results = db.session.execute(
                course_semester.select().where(course_semester.c.course_id == course.id)
            ).fetchall()
            for sr in semester_results:
                semesters.append(sr.semester)
        except Exception as e:
            pass
        
        # 如果没有从course_semester表获取到，尝试用旧的semester字段
        if not semesters and hasattr(course, 'semester') and course.semester:
            semesters = [s.strip() for s in course.semester.split('、') if s.strip()]
        
        result.append({
            'id': course.id,
            'name': course.name,
            'credit': float(course.credit),
            'description': course.description,
            'course_type': course.course_type,  # 保留旧字段，兼容旧数据
            'course_types': course_course_types_map.get(course.id, []),  # 新字段，多个课程性质
            'semesters': semesters,  # 多个学期
            'order_num': course.order_num,  # 序号
            'college': course.college or '',  # 开课学院
            'assessment_method': course.assessment_method or '闭卷笔试',  # 考核方式
            'topic_category': course.topic_category or '',  # 主题类别
            'major_ids': [m.id for m in course.majors],
            'major_names': ','.join([m.name for m in course.majors]),
            'major_course_types': major_course_types,  # 每个专业的课程性质
            'major_study_semesters': major_study_semesters,  # 每个专业的修读学期
            'teacher_ids': [t.id for t in course.teachers],
            'teacher_names': ','.join([t.name for t in course.teachers]),
            'teacher_pinyins': ','.join([t.name_pinyin or '' for t in course.teachers]),
            'teacher_ratings': teacher_avg_ratings,  # 老师评分映射
            'teacher_evaluation_counts': {str(tid): len(ratings) for tid, ratings in teacher_ratings.items()},  # 每位老师的评价人数
            'avg_rating': round(avg_rating, 1) if avg_rating else None,
            'evaluation_count': len(all_ratings)  # 评价人数
        })
    
    # 存入缓存（5分钟）
    cache.set(cache_key, result, timeout=app.config.get('CACHE_COURSES_TIMEOUT', 300))
    
    return jsonify(result)

@app.route('/api/courses', methods=['POST'])
@jwt_required()
def create_course():
    claims = get_jwt()
    if claims['role'] not in ['admin', 'superadmin']:
        return jsonify({'msg': '权限不足'}), 403
    data = request.get_json()

    import re
    teacher_names = re.split('[，,]', data.get('teacher_names', '').strip())
    if not teacher_names or teacher_names == ['']:
        return jsonify({'msg': '教师名字不能为空'}), 400

    teachers = []
    for name in teacher_names:
        name = name.strip()
        if name:
            teacher = Teacher.query.filter_by(name=name).first()
            if not teacher:
                teacher = Teacher(name=name, name_pinyin=get_name_pinyin(name))
                db.session.add(teacher)
                db.session.flush()
            teachers.append(teacher)

    # 去重
    unique_teachers = []
    seen = set()
    for teacher in teachers:
        if teacher.id not in seen:
            seen.add(teacher.id)
            unique_teachers.append(teacher)

    major_course_types = data.get('major_course_types', {})
    major_ids = data.get('major_ids', [])
    if not major_ids:
        return jsonify({'msg': '请至少选择一个专业'}), 400
    
    semesters = data.get('semesters', [])
    if not semesters:
        return jsonify({'msg': '请至少选择一个学期'}), 400
    
    course_types = data.get('course_types', [])
    if not course_types:
        # 兼容旧数据，如果没有course_types，用旧的course_type
        if data.get('course_type'):
            course_types = [data['course_type']]
        else:
            return jsonify({'msg': '请至少选择一个课程性质'}), 400

    # 创建课程，不直接关联majors
    course = Course(
        name=data['name'],
        credit=data['credit'],
        description=data.get('description', ''),
        course_type=course_types[0] if course_types else '',  # 第一个作为旧字段的值，兼容旧数据
        order_num=data.get('order_num', 0),
        college=data.get('college', ''),
        assessment_method=data.get('assessment_method', '闭卷笔试'),
        topic_category=data.get('topic_category', ''),
        teachers=unique_teachers
    )
    db.session.add(course)
    db.session.flush()

    # 关联专业并设置课程对于每个专业的性质和修读学期
    major_study_semesters = data.get('major_study_semesters', {})
    for major_id in major_ids:
        # 尝试用字符串和整数两种方式获取
        course_type_for_major = major_course_types.get(str(major_id), major_course_types.get(int(major_id), '必修'))
        db.session.execute(
            course_major.insert().values(
                course_id=course.id,
                major_id=int(major_id),
                course_type_for_major=course_type_for_major
            )
        )
        # 关联修读学期
        study_semesters = major_study_semesters.get(str(major_id), major_study_semesters.get(int(major_id), []))
        for ss in study_semesters:
            db.session.execute(
                course_major_semester.insert().values(
                    course_id=course.id,
                    major_id=int(major_id),
                    study_semester=ss
                )
            )
    
    # 关联学期
    for semester in semesters:
        db.session.execute(
            course_semester.insert().values(
                course_id=course.id,
                semester=semester
            )
        )
    
    # 关联课程性质
    for ct in course_types:
        db.session.execute(
            course_course_type.insert().values(
                course_id=course.id,
                course_type=ct
            )
        )

    db.session.commit()
    invalidate_course_cache()
    return jsonify({'id': course.id, 'msg': '课程创建成功'}), 201

@app.route('/api/teachers', methods=['GET'])
@jwt_required()
def get_teachers():
    teachers = Teacher.query.all()
    return jsonify([{'id': t.id, 'name': t.name} for t in teachers])

@app.route('/api/teachers', methods=['POST'])
@jwt_required()
def create_teacher():
    claims = get_jwt()
    if claims['role'] != 'admin':
        return jsonify({'msg': '权限不足'}), 403
    data = request.get_json()
    teacher = Teacher(name=data['name'], name_pinyin=get_name_pinyin(data['name']))
    db.session.add(teacher)
    db.session.commit()
    return jsonify({'id': teacher.id, 'msg': '教师添加成功'}), 201

@app.route('/api/evaluations', methods=['GET'])
@jwt_required()
def get_evaluations():
    course_id = request.args.get('course_id')
    query = Evaluation.query
    if course_id:
        try:
            query = query.filter_by(course_id=int(course_id))
        except ValueError:
            return jsonify({'msg': '无效的课程ID'}), 400
    evaluations = query.all()
    return jsonify([{
        'id': e.id,
        'teacher_id': e.teacher_id,
        'teacher_name': e.teacher.name,
        'teacher_pinyin': e.teacher.name_pinyin or '',
        'course_id': e.course_id,
        'course_name': e.course.name,
        'user_id': e.user_id,
        'rating': e.rating,
        'comment': e.comment,
        'created_at': e.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for e in evaluations])

@app.route('/api/evaluations', methods=['POST'])
@jwt_required()
def create_evaluation():
    claims = get_jwt()
    data = request.get_json()
    evaluation = Evaluation(
        teacher_id=data['teacher_id'],
        course_id=data['course_id'],
        user_id=claims.get('user_id'),
        rating=data['rating'],
        comment=data.get('comment', '')
    )
    db.session.add(evaluation)
    db.session.commit()
    invalidate_course_cache()
    return jsonify({'id': evaluation.id, 'msg': '评价添加成功'}), 201

@app.route('/api/evaluations/<int:eval_id>', methods=['PUT'])
@jwt_required()
def update_evaluation(eval_id):
    claims = get_jwt()
    if claims['role'] != 'admin':
        return jsonify({'msg': '权限不足'}), 403
    evaluation = Evaluation.query.get_or_404(eval_id)
    data = request.get_json()
    if 'rating' in data:
        evaluation.rating = data['rating']
    if 'comment' in data:
        evaluation.comment = data['comment']
    db.session.commit()
    invalidate_course_cache()
    return jsonify({'msg': '评价更新成功'})

@app.route('/api/evaluations/<int:eval_id>', methods=['DELETE'])
@jwt_required()
def delete_evaluation(eval_id):
    claims = get_jwt()
    evaluation = Evaluation.query.get_or_404(eval_id)
    # 管理员/超管可以删除任何评价，学生只能删除自己的评价
    if claims['role'] not in ['admin', 'superadmin']:
        if evaluation.user_id != claims.get('user_id'):
            return jsonify({'msg': '权限不足'}), 403
    db.session.delete(evaluation)
    db.session.commit()
    invalidate_course_cache()
    return jsonify({'msg': '评价删除成功'})

@app.route('/api/courses/<int:course_id>', methods=['PUT'])
@jwt_required()
def update_course(course_id):
    claims = get_jwt()
    if claims['role'] not in ['admin', 'superadmin']:
        return jsonify({'msg': '权限不足'}), 403
    data = request.get_json()
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'msg': '课程不存在'}), 404
    
    # 导入course_major表
    from models import course_major

    # 更新基本信息
    if 'name' in data:
        course.name = data['name']
    if 'credit' in data:
        course.credit = data['credit']
    if 'description' in data:
        course.description = data['description']
    if 'course_type' in data:
        course.course_type = data['course_type']
    if 'order_num' in data:
        course.order_num = data['order_num']
    if 'college' in data:
        course.college = data['college']
    if 'assessment_method' in data:
        course.assessment_method = data['assessment_method']
    if 'topic_category' in data:
        course.topic_category = data['topic_category']

    # 更新教师
    if 'teacher_names' in data:
        import re
        teacher_names = re.split('[，,]', data['teacher_names'].strip())
        teachers = []
        for name in teacher_names:
            name = name.strip()
            if name:
                teacher = Teacher.query.filter_by(name=name).first()
                if not teacher:
                    teacher = Teacher(name=name, name_pinyin=get_name_pinyin(name))
                    db.session.add(teacher)
                    db.session.flush()
                teachers.append(teacher)
        # 去重
        unique_teachers = []
        seen = set()
        for teacher in teachers:
            if teacher.id not in seen:
                seen.add(teacher.id)
                unique_teachers.append(teacher)
        course.teachers = unique_teachers

    # 更新专业关联和课程性质
    if 'major_ids' in data:
        major_course_types = data.get('major_course_types', {})
        major_study_semesters = data.get('major_study_semesters', {})
        # 先删除旧的专业关联
        db.session.execute(
            course_major.delete().where(course_major.c.course_id == course_id)
        )
        # 删除旧的修读学期关联
        try:
            db.session.execute(
                course_major_semester.delete().where(course_major_semester.c.course_id == course_id)
            )
        except:
            pass
        # 添加新的专业关联
        for major_id in data['major_ids']:
            # 尝试用字符串和整数两种方式获取
            course_type_for_major = major_course_types.get(str(major_id), major_course_types.get(int(major_id), '必修'))
            db.session.execute(
                course_major.insert().values(
                    course_id=course_id,
                    major_id=int(major_id),
                    course_type_for_major=course_type_for_major
                )
            )
            # 添加修读学期
            study_semesters = major_study_semesters.get(str(major_id), major_study_semesters.get(int(major_id), []))
            for ss in study_semesters:
                db.session.execute(
                    course_major_semester.insert().values(
                        course_id=course_id,
                        major_id=int(major_id),
                        study_semester=ss
                    )
                )
    
    # 更新学期
    if 'semesters' in data:
        semesters = data['semesters']
        # 先删除旧的学期关联
        db.session.execute(
            course_semester.delete().where(course_semester.c.course_id == course_id)
        )
        # 添加新的学期关联
        for semester in semesters:
            db.session.execute(
                course_semester.insert().values(
                    course_id=course_id,
                    semester=semester
                )
            )
    
    # 更新课程性质
    if 'course_types' in data:
        course_types = data['course_types']
        if not course_types:
            return jsonify({'msg': '请至少选择一个课程性质'}), 400
        # 先删除旧的课程性质关联
        db.session.execute(
            course_course_type.delete().where(course_course_type.c.course_id == course_id)
        )
        # 添加新的课程性质关联
        for ct in course_types:
            db.session.execute(
                course_course_type.insert().values(
                    course_id=course_id,
                    course_type=ct
                )
            )
        # 更新旧字段，兼容旧数据
        course.course_type = course_types[0] if course_types else ''

    db.session.commit()
    invalidate_course_cache()
    return jsonify({'msg': '课程更新成功'})

@app.route('/api/courses/<int:course_id>', methods=['DELETE'])
@jwt_required()
def delete_course(course_id):
    claims = get_jwt()
    if claims['role'] not in ['admin', 'superadmin']:
        return jsonify({'msg': '权限不足'}), 403
    course = Course.query.get_or_404(course_id)
    Evaluation.query.filter_by(course_id=course_id).delete()
    db.session.delete(course)
    db.session.commit()
    invalidate_course_cache()
    return jsonify({'msg': '课程删除成功'})

@app.route('/api/courses/clear', methods=['DELETE'])
@jwt_required()
def clear_courses():
    claims = get_jwt()
    if claims['role'] != 'superadmin':
        return jsonify({'msg': '权限不足'}), 403
    # 先删除所有评价
    Evaluation.query.delete()
    # 再删除所有课程
    Course.query.delete()
    db.session.commit()
    return jsonify({'msg': '所有课程已清空'})

@app.route('/api/evaluations/clear', methods=['DELETE'])
@jwt_required()
def clear_evaluations():
    claims = get_jwt()
    if claims['role'] != 'superadmin':
        return jsonify({'msg': '权限不足'}), 403
    # 删除所有评价
    Evaluation.query.delete()
    db.session.commit()
    return jsonify({'msg': '所有评价已清空'})

@app.route('/api/teachers/clear', methods=['DELETE'])
@jwt_required()
def clear_teachers():
    claims = get_jwt()
    if claims['role'] != 'superadmin':
        return jsonify({'msg': '权限不足'}), 403
    # 先清空关联表
    db.session.execute(course_teacher.delete())
    Teacher.query.delete()
    db.session.commit()
    return jsonify({'msg': '所有教师已清空'})

@app.route('/api/majors/clear', methods=['DELETE'])
@jwt_required()
def clear_majors():
    claims = get_jwt()
    if claims['role'] != 'superadmin':
        return jsonify({'msg': '权限不足'}), 403
    # 先清空关联表
    db.session.execute(course_major.delete())
    Major.query.delete()
    db.session.commit()
    return jsonify({'msg': '所有专业已清空'})

@app.route('/api/clear-all', methods=['DELETE'])
@jwt_required()
def clear_all():
    print('收到清空所有数据的请求！')
    claims = get_jwt()
    print('Claims:', claims)
    if claims['role'] != 'superadmin':
        return jsonify({'msg': '权限不足'}), 403
    # 删除所有数据（按正确顺序）
    print('开始删除数据...')
    Evaluation.query.delete()
    Course.query.delete()
    # 清空关联表
    db.session.execute(course_teacher.delete())
    db.session.execute(course_major.delete())
    Teacher.query.delete()
    Major.query.delete()
    # 保留admin和student用户
    User.query.filter(User.username.notin_(['admin', 'student'])).delete()
    db.session.commit()
    print('数据清空完成！')
    return jsonify({'msg': '所有数据已清空'})

@app.route('/api/feedbacks', methods=['POST'])
@jwt_required()
def create_feedback():
    claims = get_jwt()
    data = request.get_json()
    if not data.get('content'):
        return jsonify({'msg': '反馈内容不能为空'}), 400
    feedback = Feedback(
        user_id=claims.get('user_id'),
        content=data['content']
    )
    db.session.add(feedback)
    db.session.commit()
    return jsonify({'msg': '反馈提交成功'}), 201

@app.route('/api/feedbacks', methods=['GET'])
@jwt_required()
def get_feedbacks():
    claims = get_jwt()
    if claims['role'] in ['admin', 'superadmin']:
        feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).all()
    else:
        feedbacks = Feedback.query.filter_by(user_id=claims.get('user_id')).order_by(Feedback.created_at.desc()).all()
    result = []
    for f in feedbacks:
        user = User.query.get(f.user_id)
        result.append({
            'id': f.id,
            'user_id': f.user_id,
            'username': user.username if user else '未知用户',
            'content': f.content,
            'created_at': f.created_at.strftime('%Y-%m-%d %H:%M:%S') if f.created_at else None
        })
    return jsonify(result)

@app.route('/api/feedbacks/<int:feedback_id>', methods=['DELETE'])
@jwt_required()
def delete_feedback(feedback_id):
    claims = get_jwt()
    feedback = Feedback.query.get_or_404(feedback_id)
    if claims['role'] not in ['admin', 'superadmin']:
        if feedback.user_id != claims.get('user_id'):
            return jsonify({'msg': '权限不足'}), 403
    db.session.delete(feedback)
    db.session.commit()
    return jsonify({'msg': '反馈已删除'})

@app.route('/api/user/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    claims = get_jwt()
    user = User.query.get(claims.get('user_id'))
    if not user:
        return jsonify({'msg': '用户不存在'}), 404
    return jsonify({
        'id': user.id,
        'student_id': user.student_id,
        'real_name': user.real_name,
        'username': user.username,
        'role': user.role
    })

@app.route('/api/user/password', methods=['PUT'])
@jwt_required()
def change_password():
    claims = get_jwt()
    data = request.get_json()
    user = User.query.get(claims.get('user_id'))
    if not user:
        return jsonify({'msg': '用户不存在'}), 404
    if not data.get('old_password') or not data.get('new_password'):
        return jsonify({'msg': '请填写完整信息'}), 400
    if not (check_password_hash(user.password, data['old_password']) or user.password == data['old_password']):
        return jsonify({'msg': '原密码错误'}), 400
    if len(data['new_password']) < 6:
        return jsonify({'msg': '新密码长度不能少于6位'}), 400
    user.password = generate_password_hash(data['new_password'])
    db.session.commit()
    return jsonify({'msg': '密码修改成功'})

@app.route('/api/user/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    claims = get_jwt()
    data = request.get_json()
    user = User.query.get(claims.get('user_id'))
    if not user:
        return jsonify({'msg': '用户不存在'}), 404
    if data.get('real_name') is not None:
        user.real_name = data['real_name']
    if data.get('student_id') is not None:
        user.student_id = data['student_id']
    db.session.commit()
    return jsonify({'msg': '信息更新成功'})

@app.route('/api/user/account', methods=['DELETE'])
@jwt_required()
def delete_account():
    claims = get_jwt()
    user = User.query.get(claims.get('user_id'))
    if not user:
        return jsonify({'msg': '用户不存在'}), 404
    if user.role == 'superadmin':
        return jsonify({'msg': '超级管理员不能注销账号'}), 403
    db.session.delete(user)
    db.session.commit()
    return jsonify({'msg': '账号已注销'})

def create_app():
    return app

if __name__ == '__main__':
    init_db()
    app.run(debug=False, port=5001)
