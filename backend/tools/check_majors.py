from app import app
from models import db, Major

with app.app_context():
    majors = Major.query.all()
    print('专业列表:')
    for m in majors:
        print(f'ID: {m.id}, 名称: {m.name}')