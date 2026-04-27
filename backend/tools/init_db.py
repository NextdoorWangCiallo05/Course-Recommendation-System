"""初始化数据库并创建基础数据"""
from app import app, db
from models import Major

with app.app_context():
    db.create_all()
    print("数据库初始化成功")
    
    # 创建基础专业
    majors = ['计算机', '软件', '大数据', '人工智能', '软件（实验）', '人工智能（实验）', '公共课']
    for name in majors:
        if not Major.query.filter_by(name=name).first():
            db.session.add(Major(name=name))
    db.session.commit()
    print(f"专业数: {Major.query.count()}")
