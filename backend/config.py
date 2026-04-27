import os
from datetime import timedelta
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///course_recommendation.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)  # Token 30天过期
    TIMEZONE = 'Asia/Shanghai'  # 东八区
    
    # MySQL 连接池配置（仅在使用 MySQL 时生效）
    SQLALCHEMY_POOL_SIZE = int(os.environ.get('SQLALCHEMY_POOL_SIZE', 20))  # 连接池大小
    SQLALCHEMY_MAX_OVERFLOW = int(os.environ.get('SQLALCHEMY_MAX_OVERFLOW', 10))  # 最大溢出连接数
    SQLALCHEMY_POOL_RECYCLE = int(os.environ.get('SQLALCHEMY_POOL_RECYCLE', 3600))  # 连接回收时间（秒）
    SQLALCHEMY_POOL_PRE_PING = True  # 连接前检查连接是否有效
    
    # Redis 缓存配置
    REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
    REDIS_DB = int(os.environ.get('REDIS_DB', 0))
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', None)
    
    # 缓存开关（默认开启）
    CACHE_ENABLED = os.environ.get('CACHE_ENABLED', 'true').lower() == 'true'
    
    # 缓存过期时间（秒）
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get('CACHE_DEFAULT_TIMEOUT', 300))  # 默认5分钟
    CACHE_COURSES_TIMEOUT = int(os.environ.get('CACHE_COURSES_TIMEOUT', 300))  # 课程列表缓存5分钟
    CACHE_MAJORS_TIMEOUT = int(os.environ.get('CACHE_MAJORS_TIMEOUT', 3600))  # 专业列表缓存1小时
    CACHE_TEACHERS_TIMEOUT = int(os.environ.get('CACHE_TEACHERS_TIMEOUT', 3600))  # 教师列表缓存1小时
