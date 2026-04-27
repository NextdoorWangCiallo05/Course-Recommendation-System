@echo off
echo ========================================
echo 课程推荐系统 - 本地开发服务器
echo ========================================
echo.

REM 检查 .env 文件是否存在
if not exist ".env" (
    echo [警告] .env 文件不存在，使用默认配置
    echo [提示] 请复制 .env.example 为 .env 并修改配置
    echo.
)

REM 安装依赖（如果需要）
echo [1/3] 检查依赖...
pip install -r requirements.txt -q

REM 创建日志目录
if not exist "logs" mkdir logs

echo [2/3] 启动 Gunicorn 服务器...
echo 访问地址: http://localhost:5001
echo.

REM 启动 Gunicorn
gunicorn -c gunicorn.conf.py "app:app"

pause
