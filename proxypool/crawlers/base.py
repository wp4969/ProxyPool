import time
from lxml import etree
from retrying import retry
import requests
from loguru import logger
from ProxyPool.utils.header import Header


class BaseCrawler(object):
    urls = []

    def __init__(self):
        self.header = Header()

    @retry(stop_max_attempt_number=3, retry_on_result=lambda x: x is None, wait_fixed=2000)
    def fetch(self, url):
        try:
            response = requests.get(url, headers=self.header.get_header(), verify=False, timeout=15)
            if response.status_code == 200:
                response.encoding = 'utf-8'
                return etree.HTML(response.text)
        except requests.ConnectionError:
            return

    @logger.catch
    def crawl(self):
        for url in self.urls:
            logger.info(f'fetching {url}')
            response = self.fetch(url)
            time.sleep(0.5)
            for proxy in self.parse(response):
                logger.info(f'fetched proxy {proxy} from {url}')
                yield proxy