from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from models import db, Teacher, course_teacher
from routes.utils import invalidate_teacher_cache, get_name_pinyin

teachers_bp = Blueprint('teachers', __name__, url_prefix='/api')

@teachers_bp.route('/teachers', methods=['GET'])
@jwt_required()
def get_teachers():
    teachers = Teacher.query.all()
    return jsonify([{'id': t.id, 'name': t.name} for t in teachers])

@teachers_bp.route('/teachers', methods=['POST'])
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

@teachers_bp.route('/teachers/clear', methods=['DELETE'])
@jwt_required()
def clear_teachers():
    claims = get_jwt()
    if claims['role'] != 'superadmin':
        return jsonify({'msg': '权限不足'}), 403
    db.session.execute(course_teacher.delete())
    Teacher.query.delete()
    db.session.commit()
    invalidate_teacher_cache()
    return jsonify({'msg': '所有教师已清空'})
