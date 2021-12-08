from ProxyPool.crawlers.base import BaseCrawler

PROXY_TYPE = range(1, 3)
MAX_PAGE = 10
BASE_URL = 'http://www.kxdaili.com/dailiip/{stype}/{page}.html'


class KaiXinCrawl(BaseCrawler):
    """
    开心代理 http://www.kxdaili.com
    如果不想获取器执行这个代理 可以设置：ignore = True
    """
    urls = [BASE_URL.format(stype=stype, page=page) for stype in PROXY_TYPE for page in range(1, MAX_PAGE+1)]
    ignore = False

    def parse(self, response):
        trs = response.xpath('//table[@class="active"]/tbody/tr')
        for tr in trs:
            ip = tr.xpath('.//td[1]/text()')[0]
            port = tr.xpath('.//td[2]/text()')[0]
            proxy = '{}:{}'.format(ip, port)
            #elite = '高匿' in tr.xpath('.//td[3]/text()').get()
            #https = 'HTTPS' in tr.xpath('.//td[4]/text()').get()
            yield proxy
