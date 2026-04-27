"""
在 MySQL 中创建表结构
"""
from app import app, db
from models import *

with app.app_context():
    db.create_all()
    print('MySQL 表结构创建成功')
    
    # 列出所有表
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f'已创建的表: {tables}')
