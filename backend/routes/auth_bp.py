from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from extensions import limiter
from routes.utils import logger
import re

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        if user.role == 'pending':
            return jsonify({'msg': '账户正在审核中，请耐心等待'}), 403
        access_token = create_access_token(identity=user.username, additional_claims={'role': user.role, 'user_id': user.id})
        return jsonify(access_token=access_token, role=user.role, username=user.username, user_id=user.id), 200
    return jsonify({'msg': '用户名或密码错误'}), 401

@auth_bp.route('/register', methods=['POST'])
@limiter.limit("3 per hour")
def register():
    data = request.get_json()
    if not data.get('username') or not data.get('password') or not data.get('role'):
        return jsonify({'msg': '请填写完整信息'}), 400
    if not data.get('real_name') or not data.get('student_id'):
        return jsonify({'msg': '请填写真实姓名和学号'}), 400
    if data['role'] not in ['admin', 'student']:
        return jsonify({'msg': '角色只能是管理员或学生'}), 400
    if len(data['username']) < 3 or len(data['username']) > 20:
        return jsonify({'msg': '用户名长度需在3-20位之间'}), 400
    if not re.match(r'^[a-zA-Z0-9_]+$', data['username']):
        return jsonify({'msg': '用户名只能包含字母、数字和下划线'}), 400
    password = data['password']
    if len(password) < 8:
        return jsonify({'msg': '密码长度至少8位'}), 400
    if not re.search(r'[a-zA-Z]', password) or not re.search(r'[0-9]', password):
        return jsonify({'msg': '密码必须包含字母和数字'}), 400
    if not re.match(r'^[A-Za-z0-9]+$', data['student_id']):
        return jsonify({'msg': '学号格式不正确'}), 400
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
    logger.info(f'新用户注册等待审核: {data["username"]} ({data["real_name"]})')
    return jsonify({'msg': '注册成功，等待超级管理员审核'}), 200
