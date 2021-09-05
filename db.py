MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = 'proxies'

import redis
from random import choice

class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """初始化"""
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        """添加代理，设置分数为最高"""
        if not self.db.zscore(REDIS_KEY, proxy):
            mapping = {proxy: score, }
            return self.db.zadd(REDIS_KEY, mapping)

    def random(self):
        """随机获取有效代理"""
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)
            if len(result):
                return choice(result)

    def decrease(self, proxy):
        """代理值减一分，如果分数小于最小值，则删除代理"""
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print('Proxy: ', proxy, ' Current Score: ', score, ' -1')
            return self.db.zincrby(REDIS_KEY, proxy, -1)
        else:
            print('Proxy: ', proxy, ' Current Score: ', score, ' remove')
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        """判断是否存在"""
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def max(self, proxy):
        """将代理设置为MAX_SCORE"""
        print('Proxy ', proxy, 'available, set ', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def count(self):
        """获取代理数量"""
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """获取全部代理"""
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)
