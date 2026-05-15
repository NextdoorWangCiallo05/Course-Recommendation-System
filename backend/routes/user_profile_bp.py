from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

user_profile_bp = Blueprint('user_profile', __name__, url_prefix='/api')

@user_profile_bp.route('/user/profile', methods=['GET'])
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

@user_profile_bp.route('/user/password', methods=['PUT'])
@jwt_required()
def change_password():
    claims = get_jwt()
    data = request.get_json()
    user = User.query.get(claims.get('user_id'))
    if not user:
        return jsonify({'msg': '用户不存在'}), 404
    if not data.get('old_password') or not data.get('new_password'):
        return jsonify({'msg': '请填写完整信息'}), 400
    if not check_password_hash(user.password, data['old_password']):
        return jsonify({'msg': '原密码错误'}), 400
    if len(data['new_password']) < 6:
        return jsonify({'msg': '新密码长度不能少于6位'}), 400
    user.password = generate_password_hash(data['new_password'])
    db.session.commit()
    return jsonify({'msg': '密码修改成功'})

@user_profile_bp.route('/user/profile', methods=['PUT'])
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

@user_profile_bp.route('/user/account', methods=['DELETE'])
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
