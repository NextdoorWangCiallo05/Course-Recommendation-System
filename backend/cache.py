"""
Redis 缓存工具模块
提供简单的缓存装饰器和缓存操作函数
"""
import json
import redis
import logging
from functools import wraps
from flask import request

logger = logging.getLogger(__name__)

class CacheManager:
    """Redis 缓存管理器"""
    
    def __init__(self, app=None):
        self.redis_client = None
        self.enabled = False
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """初始化 Redis 连接"""
        self.enabled = app.config.get('CACHE_ENABLED', True)
        
        if not self.enabled:
            logger.info('缓存已禁用')
            return
        
        try:
            self.redis_client = redis.Redis(
                host=app.config.get('REDIS_HOST', 'localhost'),
                port=app.config.get('REDIS_PORT', 6379),
                db=app.config.get('REDIS_DB', 0),
                password=app.config.get('REDIS_PASSWORD', None),
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True
            )
            # 测试连接
            self.redis_client.ping()
            logger.info('Redis 连接成功')
        except redis.ConnectionError as e:
            logger.warning(f'Redis 连接失败，缓存功能将不可用: {e}')
            self.enabled = False
            self.redis_client = None
    
    def get(self, key):
        """获取缓存"""
        if not self.enabled or not self.redis_client:
            return None
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f'获取缓存失败: {e}')
            return None
    
    def set(self, key, value, timeout=300):
        """设置缓存"""
        if not self.enabled or not self.redis_client:
            return False
        try:
            self.redis_client.setex(key, timeout, json.dumps(value))
            return True
        except Exception as e:
            logger.error(f'设置缓存失败: {e}')
            return False
    
    def delete(self, key):
        """删除缓存"""
        if not self.enabled or not self.redis_client:
            return False
        try:
            self.redis_client.delete(key)
            return True
        except Exception as e:
            logger.error(f'删除缓存失败: {e}')
            return False
    
    def delete_pattern(self, pattern):
        """删除匹配模式的缓存"""
        if not self.enabled or not self.redis_client:
            return False
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
            return True
        except Exception as e:
            logger.error(f'删除缓存模式失败: {e}')
            return False
    
    def cache_result(self, timeout=300, key_prefix='cache'):
        """
        缓存装饰器
        用法: @cache.cache_result(timeout=300, key_prefix='courses')
        """
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if not self.enabled:
                    return f(*args, **kwargs)
                
                # 生成缓存键
                cache_key = f"{key_prefix}:{f.__name__}"
                
                # 尝试从缓存获取
                cached = self.get(cache_key)
                if cached is not None:
                    logger.debug(f'缓存命中: {cache_key}')
                    return cached
                
                # 执行函数
                result = f(*args, **kwargs)
                
                # 存入缓存
                if result is not None:
                    self.set(cache_key, result, timeout)
                    logger.debug(f'缓存设置: {cache_key}')
                
                return result
            return decorated_function
        return decorator


# 全局缓存实例
cache = CacheManager()
