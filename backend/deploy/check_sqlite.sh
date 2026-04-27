#!/bin/bash
# 检查 SQLite 数据
cd /home/ubuntu/Select/backend
python3 << 'PYEOF'
import sqlite3
conn = sqlite3.connect('instance/course_recommendation.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
for t in tables:
    cursor.execute(f'SELECT COUNT(*) FROM {t[0]}')
    count = cursor.fetchone()[0]
    print(f'{t[0]}: {count} records')
conn.close()
PYEOF
