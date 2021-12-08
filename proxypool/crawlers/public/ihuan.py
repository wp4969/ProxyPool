import time
from ProxyPool.crawlers.base import BaseCrawler

PROXY_TYPE = time.strftime("%Y/%m/%d/%H", time.localtime())
BASE_URL = 'https://ip.ihuan.me/today/{}.html'


class IHuanCrawl(BaseCrawler):
    """
    小幻代理 https://ip.ihuan.me
    如果不想获取器执行这个代理 可以设置：ignore = True
    """
    urls = [BASE_URL.format(PROXY_TYPE)]
    ignore = False

    def parse(self, response):
        trs = response.xpath('//p[@class="text-left"]/text()')
        for tr in trs:
            proxy = tr.split('@')[0]
            yield proxy

