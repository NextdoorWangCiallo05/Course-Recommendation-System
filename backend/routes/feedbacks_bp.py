from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from models import db, User, Feedback

feedbacks_bp = Blueprint('feedbacks', __name__, url_prefix='/api')

@feedbacks_bp.route('/feedbacks', methods=['POST'])
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

@feedbacks_bp.route('/feedbacks', methods=['GET'])
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

@feedbacks_bp.route('/feedbacks/<int:feedback_id>', methods=['DELETE'])
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
