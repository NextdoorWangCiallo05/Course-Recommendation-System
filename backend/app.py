from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt
from werkzeug.security import generate_password_hash
from config import Config
from models import db, User, Major
from cache import cache
from extensions import jwt, limiter
from routes import register_blueprints
from routes.utils import logger
from sqlalchemy import inspect

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, origins=['https://courselect.xyz', 'https://www.courselect.xyz', 'http://courselect.xyz', 'http://www.courselect.xyz', 'http://localhost:8080', 'http://localhost', 'http://127.0.0.1'])
db.init_app(app)
jwt.init_app(app)
cache.init_app(app)
limiter.init_app(app)

register_blueprints(app)


@app.before_request
def log_request():
    if request.path.startswith('/api/'):
        logger.info(f'{request.method} {request.path} - {request.remote_addr}')


@app.after_request
def log_response(response):
    if request.path.startswith('/api/'):
        logger.info(f'{request.method} {request.path} - {response.status_code}')
    return response


def init_db():
    with app.app_context():
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()

        if len(tables) == 0:
            logger.info('数据库为空，正在初始化...')
            db.create_all()
            db.session.commit()

            users = [
                User(username='admin', password=generate_password_hash('admin123'), role='admin'),
                User(username='student', password=generate_password_hash('student123'), role='student')
            ]
            db.session.add_all(users)
            db.session.flush()

            majors = [
                Major(name='公共课', description='全校公共基础课程'),
                Major(name='计算机', description='计算机科学与技术专业课程'),
                Major(name='软件', description='软件工程专业课程'),
                Major(name='大数据', description='大数据技术专业课程'),
                Major(name='人工智能', description='人工智能专业课程')
            ]
            db.session.add_all(majors)
            db.session.commit()
            logger.info('数据库初始化完成！（包含用户和基本专业）')
        else:
            logger.info('数据库已存在，跳过初始化')
            db.create_all()
            db.session.commit()

            superadmin = User.query.filter_by(username='superadmin').first()
            if not superadmin:
                superadmin = User(username='superadmin', password=generate_password_hash('superadmin123'), role='superadmin')
                db.session.add(superadmin)
                db.session.commit()
                logger.info('超级管理员账户已创建：superadmin / superadmin123')


@app.route('/api/clear-all', methods=['DELETE'])
@jwt_required()
def clear_all():
    claims = get_jwt()
    logger.warning(f'收到清空所有数据的请求！Claims: {claims}')
    if claims['role'] != 'superadmin':
        return jsonify({'msg': '权限不足'}), 403
    from models import Teacher, Evaluation, Course, Major, User, course_major, course_teacher
    logger.warning('开始删除数据...')
    Evaluation.query.delete()
    Course.query.delete()
    db.session.execute(course_teacher.delete())
    db.session.execute(course_major.delete())
    Teacher.query.delete()
    Major.query.delete()
    User.query.filter(User.username.notin_(['admin', 'student'])).delete()
    db.session.commit()
    logger.warning('数据清空完成！')
    return jsonify({'msg': '所有数据已清空'})


if __name__ == '__main__':
    init_db()
    app.run(debug=False, port=5001)
