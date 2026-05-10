#!/bin/sh
set -e

echo "等待 MySQL 就绪..."
MAX_RETRIES=60
RETRY_COUNT=0
until python -c "
import pymysql, sys
try:
    conn = pymysql.connect(
        host='mysql',
        port=3306,
        user='root',
        password='RootPass2026!',
        connect_timeout=3
    )
    conn.close()
    sys.exit(0)
except Exception as e:
    sys.exit(1)
" 2>/dev/null; do
    RETRY_COUNT=$((RETRY_COUNT + 1))
    if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
        echo "MySQL 启动超时，放弃等待"
        exit 1
    fi
    echo "等待 MySQL 启动中... ($RETRY_COUNT/$MAX_RETRIES)"
    sleep 2
done
echo "MySQL 已就绪"

echo "正在初始化数据库..."
python -c "from app import init_db; init_db()"

echo "启动 Gunicorn..."
exec gunicorn -c gunicorn.conf.py "app:app"
