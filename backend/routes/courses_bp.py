from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy import func
from models import db, Course, Teacher, Evaluation, Major, course_major, course_teacher, course_semester, course_course_type, course_major_semester
from routes.utils import logger, invalidate_course_cache, get_name_pinyin
import re

courses_bp = Blueprint('courses', __name__, url_prefix='/api')

@courses_bp.route('/courses', methods=['GET'])
@jwt_required()
def get_courses():
    major_id = request.args.get('major_id')
    sort_order = request.args.get('sort', 'asc')
    course_type_filter = request.args.get('course_type')
    major_course_type_filter = request.args.get('major_course_type')

    from cache import cache
    cache_key = f"courses:list:major={major_id}:sort={sort_order}:ct={course_type_filter}:mct={major_course_type_filter}"
    cached = cache.get(cache_key)
    if cached is not None:
        return jsonify(cached)

    query = Course.query
    if major_id:
        try:
            query = query.filter(Course.majors.any(id=int(major_id)))
        except ValueError:
            return jsonify({'msg': '无效的专业ID'}), 400

    if sort_order == 'desc':
        all_courses = query.order_by(Course.order_num.desc()).all()
    else:
        all_courses = query.order_by(Course.order_num.asc()).all()

    course_types = []
    if course_type_filter:
        course_types = [ct.strip() for ct in course_type_filter.split(',') if ct.strip()]

    filtered_courses = []
    for course in all_courses:
        course_course_types = []
        try:
            ct_results = db.session.execute(
                course_course_type.select().where(course_course_type.c.course_id == course.id)
            ).fetchall()
            for ct in ct_results:
                course_course_types.append(ct.course_type)
        except:
            pass

        if not course_course_types and hasattr(course, 'course_type') and course.course_type:
            course_course_types = [course.course_type]

        if course_types:
            has_match = False
            for ct in course_types:
                if ct in course_course_types:
                    has_match = True
                    break
            if not has_match:
                continue

        if major_id and major_course_type_filter:
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
        teacher_ratings = {}
        evaluations = Evaluation.query.filter_by(course_id=course.id).all()
        for eval in evaluations:
            teacher_id = eval.teacher_id
            if teacher_id not in teacher_ratings:
                teacher_ratings[teacher_id] = []
            teacher_ratings[teacher_id].append(eval.rating)

        teacher_avg_ratings = {}
        for teacher_id, ratings in teacher_ratings.items():
            teacher_avg_ratings[teacher_id] = round(sum(ratings) / len(ratings), 1)

        all_ratings = [r for ratings in teacher_ratings.values() for r in ratings]
        avg_rating = sum(all_ratings) / len(all_ratings) if all_ratings else None

        major_course_types = {}
        major_study_semesters = {}

        for major in course.majors:
            course_major_result = db.session.execute(
                course_major.select().where(
                    course_major.c.course_id == course.id,
                    course_major.c.major_id == major.id
                )
            ).fetchone()
            if course_major_result:
                major_course_types[major.id] = course_major_result.course_type_for_major
            else:
                major_course_types[major.id] = '必修'

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

        main_major_ids = [1, 2, 3, 4, 5, 6, 7, 8]
        for mid in main_major_ids:
            try:
                cms_results = db.session.execute(
                    course_major_semester.select().where(
                        course_major_semester.c.course_id == course.id,
                        course_major_semester.c.major_id == mid
                    )
                ).fetchall()
                if cms_results:
                    major_study_semesters[mid] = [r.study_semester for r in cms_results]
            except:
                pass

        try:
            cms_results = db.session.execute(
                course_major_semester.select().where(
                    course_major_semester.c.course_id == course.id,
                    course_major_semester.c.major_id == 1
                )
            ).fetchall()
            if cms_results:
                major_study_semesters[1] = [r.study_semester for r in cms_results]
        except:
            pass

        try:
            cms_results = db.session.execute(
                course_major_semester.select().where(
                    course_major_semester.c.course_id == course.id,
                    course_major_semester.c.major_id == 7
                )
            ).fetchall()
            if cms_results:
                major_study_semesters[7] = [r.study_semester for r in cms_results]
        except:
            pass

        result.append({
            'id': course.id,
            'name': course.name,
            'credit': float(course.credit),
            'description': course.description or '',
            'course_type': course.course_type,
            'semester': course.semester,
            'order_num': course.order_num,
            'college': course.college or '',
            'assessment_method': course.assessment_method or '',
            'topic_category': course.topic_category or '',
            'teachers': [{'id': t.id, 'name': t.name, 'name_pinyin': t.name_pinyin or ''} for t in course.teachers],
            'majors': [{'id': m.id, 'name': m.name} for m in course.majors],
            'major_course_types': major_course_types,
            'major_study_semesters': major_study_semesters,
            'course_types': course_course_types_map.get(course.id, []),
            'semesters': [s.semester for s in db.session.execute(course_semester.select().where(course_semester.c.course_id == course.id)).fetchall()],
            'avg_rating': round(avg_rating, 1) if avg_rating else None,
            'teacher_avg_ratings': teacher_avg_ratings,
            'evaluations': [{
                'id': e.id,
                'teacher_id': e.teacher_id,
                'teacher_name': e.teacher.name,
                'rating': e.rating,
                'comment': e.comment,
                'created_at': e.created_at.strftime('%Y-%m-%d %H:%M:%S') if e.created_at else ''
            } for e in evaluations]
        })

    cache.set(cache_key, result, timeout=300)
    return jsonify(result)

@courses_bp.route('/courses', methods=['POST'])
@jwt_required()
def create_course():
    claims = get_jwt()
    if claims['role'] not in ['admin', 'superadmin']:
        return jsonify({'msg': '权限不足'}), 403
    data = request.get_json()

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

    unique_teachers = []
    seen = set()
    for teacher in teachers:
        if teacher.id not in seen:
            seen.add(teacher.id)
            unique_teachers.append(teacher)

    major_ids = data.get('major_ids', [])
    if not major_ids:
        return jsonify({'msg': '请至少选择一个专业'}), 400

    semesters = data.get('semesters', [])
    if not semesters:
        return jsonify({'msg': '请至少选择一个学期'}), 400

    course_types = data.get('course_types', [])
    if not course_types:
        if data.get('course_type'):
            course_types = [data['course_type']]
        else:
            return jsonify({'msg': '请至少选择一个课程性质'}), 400

    course = Course(
        name=data['name'],
        credit=data['credit'],
        description=data.get('description', ''),
        course_type=course_types[0] if course_types else '',
        order_num=data.get('order_num', 0),
        college=data.get('college', ''),
        assessment_method=data.get('assessment_method', '闭卷笔试'),
        topic_category=data.get('topic_category', ''),
        teachers=unique_teachers
    )
    db.session.add(course)
    db.session.flush()

    major_course_types = data.get('major_course_types', {})
    major_study_semesters = data.get('major_study_semesters', {})
    for major_id in major_ids:
        course_type_for_major = major_course_types.get(str(major_id), major_course_types.get(int(major_id), '必修'))
        db.session.execute(
            course_major.insert().values(
                course_id=course.id,
                major_id=int(major_id),
                course_type_for_major=course_type_for_major
            )
        )
        study_semesters = major_study_semesters.get(str(major_id), major_study_semesters.get(int(major_id), []))
        for ss in study_semesters:
            db.session.execute(
                course_major_semester.insert().values(
                    course_id=course.id,
                    major_id=int(major_id),
                    study_semester=ss
                )
            )

    for semester in semesters:
        db.session.execute(
            course_semester.insert().values(course_id=course.id, semester=semester)
        )

    for ct in course_types:
        db.session.execute(
            course_course_type.insert().values(course_id=course.id, course_type=ct)
        )

    db.session.commit()
    invalidate_course_cache()
    return jsonify({'id': course.id, 'msg': '课程创建成功'}), 201

@courses_bp.route('/courses/<int:course_id>', methods=['PUT'])
@jwt_required()
def update_course(course_id):
    claims = get_jwt()
    if claims['role'] not in ['admin', 'superadmin']:
        return jsonify({'msg': '权限不足'}), 403
    data = request.get_json()
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'msg': '课程不存在'}), 404

    if 'name' in data:
        course.name = data['name']
    if 'credit' in data:
        course.credit = data['credit']
    if 'description' in data:
        course.description = data['description']
    if 'order_num' in data:
        course.order_num = data['order_num']
    if 'college' in data:
        course.college = data['college']
    if 'assessment_method' in data:
        course.assessment_method = data['assessment_method']
    if 'topic_category' in data:
        course.topic_category = data['topic_category']

    if 'teacher_names' in data:
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
        unique_teachers = []
        seen = set()
        for teacher in teachers:
            if teacher.id not in seen:
                seen.add(teacher.id)
                unique_teachers.append(teacher)
        course.teachers = unique_teachers

    if 'major_ids' in data:
        major_course_types = data.get('major_course_types', {})
        major_study_semesters = data.get('major_study_semesters', {})
        db.session.execute(course_major.delete().where(course_major.c.course_id == course_id))
        try:
            db.session.execute(course_major_semester.delete().where(course_major_semester.c.course_id == course_id))
        except:
            pass
        for major_id in data['major_ids']:
            course_type_for_major = major_course_types.get(str(major_id), major_course_types.get(int(major_id), '必修'))
            db.session.execute(
                course_major.insert().values(
                    course_id=course_id,
                    major_id=int(major_id),
                    course_type_for_major=course_type_for_major
                )
            )
            study_semesters = major_study_semesters.get(str(major_id), major_study_semesters.get(int(major_id), []))
            for ss in study_semesters:
                db.session.execute(
                    course_major_semester.insert().values(
                        course_id=course_id,
                        major_id=int(major_id),
                        study_semester=ss
                    )
                )

    if 'semesters' in data:
        db.session.execute(course_semester.delete().where(course_semester.c.course_id == course_id))
        for semester in data['semesters']:
            db.session.execute(course_semester.insert().values(course_id=course_id, semester=semester))

    if 'course_types' in data:
        course_types = data['course_types']
        if not course_types:
            return jsonify({'msg': '请至少选择一个课程性质'}), 400
        db.session.execute(course_course_type.delete().where(course_course_type.c.course_id == course_id))
        for ct in course_types:
            db.session.execute(course_course_type.insert().values(course_id=course_id, course_type=ct))
        course.course_type = course_types[0] if course_types else ''

    db.session.commit()
    invalidate_course_cache()
    return jsonify({'msg': '课程更新成功'})

@courses_bp.route('/courses/<int:course_id>', methods=['DELETE'])
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

@courses_bp.route('/courses/clear', methods=['DELETE'])
@jwt_required()
def clear_courses():
    claims = get_jwt()
    if claims['role'] != 'superadmin':
        return jsonify({'msg': '权限不足'}), 403
    Evaluation.query.delete()
    Course.query.delete()
    db.session.commit()
    return jsonify({'msg': '所有课程已清空'})
