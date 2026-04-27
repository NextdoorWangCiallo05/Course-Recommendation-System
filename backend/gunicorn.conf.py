# Gunicorn 配置文件
# 用于生产环境部署

import multiprocessing

# 服务器绑定
bind = "0.0.0.0:5001"

# 工作进程数（CPU核心数 * 2 + 1）
workers = 4

# 工作进程类型（sync 兼容 Windows）
worker_class = "sync"

# 超时时间（秒）
timeout = 120

# 保持连接数
keepalive = 5

# 日志配置
accesslog = "logs/gunicorn_access.log"
errorlog = "logs/gunicorn_error.log"
loglevel = "info"

# 进程命名
proc_name = "course_recommendation"

# 守护进程模式
daemon = False

# 预加载应用（提高性能）
preload_app = True

# 优雅重启超时
graceful_timeout = 30
