from loguru import logger
from ProxyPool.crawlers import __all__ as crawlers_cls
from ProxyPool.components.redisclient import RedisClient
from ProxyPool.setting import PROXY_NUMBER_MAX, LOGGER_ENABLED, LOGGER_FILE, LOGGER_LEVEL, \
    LOGGER_FORMAT, LOGGER_RETENTION, LOGGER_ROTATION


class Getter:
    """
    获取模块: 获取所有的代理并存储到redis中
    """
    def __init__(self):
        self.redis = RedisClient()
        self.crawlers_cls = crawlers_cls
        self.crawlers = [crawler_cls() for crawler_cls in self.crawlers_cls]
        if LOGGER_ENABLED:
            logger.add(LOGGER_FILE, level=LOGGER_LEVEL, format=LOGGER_FORMAT, retention=LOGGER_RETENTION,
                       rotation=LOGGER_ROTATION)

    def is_full(self):
        return self.redis.count() >= PROXY_NUMBER_MAX

    @logger.catch
    def run(self):
        if self.is_full():
            return
        for crawler in self.crawlers:
            for proxy in crawler.crawl():
                logger.info(f'crawler {crawler} to get proxys')
                self.redis.add(proxy)


if __name__ == '__main__':
    getter = Getter()
    getter.run()
