from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from models import db, Teacher, Evaluation, Major, Course, course_course_type, course_major

stats_bp = Blueprint('stats', __name__, url_prefix='/api')

@stats_bp.route('/stats/teacher-ratings', methods=['GET'])
@jwt_required()
def stats_teacher_ratings():
    results = db.session.query(
        Teacher.id,
        Teacher.name,
        func.coalesce(func.avg(Evaluation.rating), 0).label('avg_rating'),
        func.count(Evaluation.id).label('eval_count')
    ).outerjoin(Evaluation).group_by(Teacher.id).order_by(func.avg(Evaluation.rating).desc()).all()
    return jsonify([{
        'id': r.id, 'name': r.name,
        'avg_rating': round(float(r.avg_rating), 1),
        'eval_count': r.eval_count
    } for r in results])

@stats_bp.route('/stats/course-types', methods=['GET'])
@jwt_required()
def stats_course_types():
    results = db.session.query(
        course_course_type.c.course_type,
        func.count(course_course_type.c.course_id).label('count')
    ).group_by(course_course_type.c.course_type).all()
    return jsonify([{'type': r.course_type, 'count': r.count} for r in results])

@stats_bp.route('/stats/major-courses', methods=['GET'])
@jwt_required()
def stats_major_courses():
    results = db.session.query(
        Major.name,
        func.count(course_major.c.course_id).label('count')
    ).join(Major).group_by(Major.id).all()
    return jsonify([{'major': r.name, 'count': r.count} for r in results])

@stats_bp.route('/stats/eval-trend', methods=['GET'])
@jwt_required()
def stats_eval_trend():
    results = db.session.query(
        func.date(Evaluation.created_at).label('date'),
        func.count(Evaluation.id).label('count'),
        func.avg(Evaluation.rating).label('avg_rating')
    ).filter(Evaluation.created_at.isnot(None)).group_by(func.date(Evaluation.created_at)).order_by(func.date(Evaluation.created_at)).all()
    return jsonify([{
        'date': str(r.date),
        'count': r.count,
        'avg_rating': round(float(r.avg_rating), 1) if r.avg_rating else 0
    } for r in results])

@stats_bp.route('/stats/credit-summary', methods=['GET'])
@jwt_required()
def stats_credit_summary():
    major_credits = db.session.query(
        Major.name,
        func.sum(Course.credit).label('total_credits'),
        func.count(Course.id).label('course_count')
    ).select_from(Major).join(course_major, Major.id == course_major.c.major_id).join(Course, Course.id == course_major.c.course_id).group_by(Major.id).all()

    type_credits = db.session.query(
        course_course_type.c.course_type,
        func.sum(Course.credit).label('total_credits'),
        func.count(Course.id).label('course_count')
    ).join(Course, Course.id == course_course_type.c.course_id).group_by(course_course_type.c.course_type).all()

    return jsonify({
        'major_credits': [{
            'major': r.name,
            'total_credits': float(r.total_credits) if r.total_credits else 0,
            'course_count': r.course_count
        } for r in major_credits],
        'type_credits': [{
            'type': r.course_type,
            'total_credits': float(r.total_credits) if r.total_credits else 0,
            'course_count': r.course_count
        } for r in type_credits]
    })
