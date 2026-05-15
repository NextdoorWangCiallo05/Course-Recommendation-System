from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash
from models import db, User
from routes.utils import logger, invalidate_major_cache, mask_student_id, mask_real_name

users_bp = Blueprint('users', __name__, url_prefix='/api')

@users_bp.route('/users', methods=['GET'])
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

@users_bp.route('/users', methods=['POST'])
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

@users_bp.route('/users/<int:user_id>/approve', methods=['PUT'])
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

@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
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

@users_bp.route('/notifications/pending-users', methods=['GET'])
@jwt_required()
def get_pending_users_notification():
    claims = get_jwt()
    if claims['role'] not in ['admin', 'superadmin']:
        return jsonify({'msg': '权限不足'}), 403
    pending = User.query.filter_by(role='pending').all()
    return jsonify({
        'count': len(pending),
        'users': [{
            'id': u.id,
            'username': u.username,
            'real_name': u.real_name or '',
            'requested_role': u.requested_role or '',
            'created_at': u.created_at.strftime('%Y-%m-%d %H:%M:%S') if u.created_at else ''
        } for u in pending]
    })

@users_bp.route('/users/<int:user_id>/role', methods=['PUT'])
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
