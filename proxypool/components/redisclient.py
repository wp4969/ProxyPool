import redis
import random
from loguru import logger
from proxypool.setting import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_KEY, REDIS_PASSWD, MIN_SCORE, MAX_SCORE, AMOUNT_SCORE, \
    LOGGER_ENABLED, LOGGER_FILE, LOGGER_LEVEL, LOGGER_FORMAT, LOGGER_RETENTION, LOGGER_ROTATION


class RedisClient:
    """
    存储模块: 操作redis的所有方法
    """
    def __init__(self):
        self.db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWD, decode_responses=True)
        if LOGGER_ENABLED:
            logger.add(LOGGER_FILE, level=LOGGER_LEVEL, format=LOGGER_FORMAT, retention=LOGGER_RETENTION,
                       rotation=LOGGER_ROTATION)

    def add(self, proxy) -> int:
        if not self.exists(proxy):
            return self.db.zadd(REDIS_KEY, {proxy: MAX_SCORE})

    def max(self, proxy):
        return self.db.zadd(REDIS_KEY, {proxy: MAX_SCORE})

    def increment(self, proxy):
        self.db.zincrby(REDIS_KEY, AMOUNT_SCORE, proxy)
        score = self.db.zscore(REDIS_KEY, proxy)
        if score <= MIN_SCORE:
            self.db.zrem(REDIS_KEY, proxy)

    @logger.catch
    def random(self):
        proxies = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(proxies):
            return proxies[random.randint(0, len(proxies)-1)]

    @logger.catch
    def all(self):
        return self.db.zrevrangebyscore(REDIS_KEY, MAX_SCORE, MIN_SCORE)

    def exists(self, proxy):
        return not self.db.zscore(REDIS_KEY, proxy) is None

    def delete(self):
        return self.db.zremrangebyscore(REDIS_KEY, MIN_SCORE, MIN_SCORE)

    def count(self):
        return self.db.zcard(REDIS_KEY)

    @logger.catch
    def counts(self):
        proxy_count = self.db.zcount(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        test_count = self.db.zcount(REDIS_KEY, MIN_SCORE, MAX_SCORE-1)
        return {'proxy': proxy_count, 'test': test_count}

    def batch(self, cursor, count):
        """
        获取一批代理
        cursor: scan游标
        count: scan总数
        """
        cursor, proxies = self.db.zscan(REDIS_KEY, cursor, count=count)
        return cursor, proxies

if __name__ == '__main__':
    a = RedisClient()
    print(a.random('proxy_elite'))