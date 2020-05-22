import redis

from settings import REDIS_PWD

__all__ = ['r']


pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)
r = redis.StrictRedis(connection_pool=pool)

# r = redis.StrictRedis(host='127.0.0.1', port=6379, decode_responses=True, password=REDIS_PWD)