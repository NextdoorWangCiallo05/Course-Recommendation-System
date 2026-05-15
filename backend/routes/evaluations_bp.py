from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from models import db, Evaluation
from routes.utils import invalidate_course_cache

evaluations_bp = Blueprint('evaluations', __name__, url_prefix='/api')

@evaluations_bp.route('/evaluations', methods=['GET'])
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

@evaluations_bp.route('/evaluations', methods=['POST'])
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

@evaluations_bp.route('/evaluations/<int:eval_id>', methods=['PUT'])
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

@evaluations_bp.route('/evaluations/<int:eval_id>', methods=['DELETE'])
@jwt_required()
def delete_evaluation(eval_id):
    claims = get_jwt()
    evaluation = Evaluation.query.get_or_404(eval_id)
    if claims['role'] not in ['admin', 'superadmin']:
        if evaluation.user_id != claims.get('user_id'):
            return jsonify({'msg': '权限不足'}), 403
    db.session.delete(evaluation)
    db.session.commit()
    invalidate_course_cache()
    return jsonify({'msg': '评价删除成功'})

@evaluations_bp.route('/evaluations/clear', methods=['DELETE'])
@jwt_required()
def clear_evaluations():
    claims = get_jwt()
    if claims['role'] != 'superadmin':
        return jsonify({'msg': '权限不足'}), 403
    Evaluation.query.delete()
    db.session.commit()
    return jsonify({'msg': '所有评价已清空'})
