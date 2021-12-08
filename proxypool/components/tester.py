import asyncio
from loguru import logger
import aiohttp
from aiohttp import ClientError, ClientConnectorError, ClientProxyConnectionError, ServerDisconnectedError, \
    ClientOSError, ClientHttpProxyError
from ProxyPool.components.redisclient import RedisClient
from ProxyPool.utils.header import Header
from ProxyPool.setting import TEST_BATCH, TEST_ANONYMOUS, TEST_TIMEOUT, TEST_URL, TEST_VALID_STATUS, \
    LOGGER_ENABLED, LOGGER_FILE, LOGGER_LEVEL, LOGGER_FORMAT, LOGGER_RETENTION, LOGGER_ROTATION


EXCEPTIONS = (
    ClientProxyConnectionError,
    ConnectionRefusedError,
    TimeoutError,
    ServerDisconnectedError,
    ClientOSError,
    ClientHttpProxyError,
    AssertionError
)


class Tester(object):
    """
    检测模块: 检测redis中所有proxy
    """
    def __init__(self):
        self.redis = RedisClient()
        self.loop = asyncio.get_event_loop()
        self.header = Header()
        if LOGGER_ENABLED:
            logger.add(LOGGER_FILE, level=LOGGER_LEVEL, format=LOGGER_FORMAT, retention=LOGGER_RETENTION,
                       rotation=LOGGER_ROTATION)

    async def test(self, proxy):
        """
        测试单个代理
        """
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            try:
                if TEST_ANONYMOUS:
                    url = 'https://httpbin.org/ip'
                    async with session.get(url, timeout=TEST_TIMEOUT) as response:
                        resp_json = await response.json()
                        origin_ip = resp_json['origin']
                    async with session.get(url, headers=self.header.get_header(), proxy=f'http://{proxy}', timeout=TEST_TIMEOUT) as response:
                        resp_json = await response.json()
                        anonymous_ip = resp_json['origin']
                    assert origin_ip != anonymous_ip
                    assert proxy.split(':')[0] == anonymous_ip
                async with session.get(TEST_URL, headers=self.header.get_header(), proxy=f'http://{proxy}', timeout=TEST_TIMEOUT, allow_redirects=False) as response:
                    if response.status in TEST_VALID_STATUS:
                        self.redis.max(proxy)
                        logger.debug(f'proxys {proxy} is valid, set max score')
                    else:
                        self.redis.increment(proxy)
                        logger.debug(f'proxys {proxy} is invalid, increment score')
            except Exception as e:
                self.redis.increment(proxy)
                logger.debug(f'proxys {proxy} is invalid, decrease score')
                logger.debug(e)

    @logger.catch
    def run(self):
        """
        测试主函数
        """
        logger.info('stating tester...')
        count = self.redis.count()
        logger.debug(f'{count} proxies to test')
        cursor = 0
        while True:
            logger.debug(f'testing proxies use cursor {cursor}, count {TEST_BATCH}')
            cursor, proxies = self.redis.batch(cursor, count=TEST_BATCH)
            if proxies:
                tasks = [self.test(proxy[0]) for proxy in proxies]
                self.loop.run_until_complete(asyncio.wait(tasks))
            if not cursor:
                break


if __name__ == '__main__':
    tester = Tester()
    tester.run()