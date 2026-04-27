#!/bin/bash
# 查看 SQLite 用户数据
cd /home/ubuntu/Select/backend
python3 << 'PYEOF'
import sqlite3
conn = sqlite3.connect('instance/course_recommendation.db')
cursor = conn.cursor()
cursor.execute("SELECT id, username, role, real_name FROM users")
users = cursor.fetchall()
for u in users:
    print(f'id={u[0]}, username={u[1]}, role={u[2]}, real_name={u[3]}')
conn.close()
PYEOF
