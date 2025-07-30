# -*- coding: utf-8 -*-
import os
import logging

from .decator import singleton

LOGGER = logging.getLogger('RedisClient')


class Redis(object):
    """
    Redis客户端简易封装（单例）
    """

    def __init__(self, redis_uri=None, redis_db=None, decode_responses=True):
        import redis

        if not redis_uri:
            redis_uri: str = os.getenv('RES_REDIS_URL')
        if not redis_db:
            redis_db: str = os.getenv('RES_REDIS_DB')
        self.client = redis.Redis.from_url(url=redis_uri, db=redis_db, decode_responses=decode_responses)
        LOGGER.info(f'init resources redis client: uri={redis_uri}, db={redis_db}')

    # 关闭链接
    def close(self):
        if self.client:
            try:
                self.client.close()
            except Exception as e:
                print(e)


@singleton
class SingletonRedis(Redis):
    def __init__(self, redis_uri=None, redis_db=None, decode_responses=True, *args, **kwargs):
        super().__init__(redis_uri=redis_uri, redis_db=redis_db, decode_responses=decode_responses, *args, **kwargs)
