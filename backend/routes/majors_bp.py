from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from models import db, Major, course_major
from routes.utils import invalidate_major_cache

majors_bp = Blueprint('majors', __name__, url_prefix='/api')

@majors_bp.route('/majors', methods=['GET'])
@jwt_required()
def get_majors():
    from cache import cache
    cached = cache.get('majors:list')
    if cached is not None:
        return jsonify(cached)
    majors = Major.query.all()
    result = [{'id': m.id, 'name': m.name, 'description': m.description} for m in majors]
    cache.set('majors:list', result, timeout=3600)
    return jsonify(result)

@majors_bp.route('/majors/clear', methods=['DELETE'])
@jwt_required()
def clear_majors():
    claims = get_jwt()
    if claims['role'] != 'superadmin':
        return jsonify({'msg': '权限不足'}), 403
    db.session.execute(course_major.delete())
    Major.query.delete()
    db.session.commit()
    invalidate_major_cache()
    return jsonify({'msg': '所有专业已清空'})
