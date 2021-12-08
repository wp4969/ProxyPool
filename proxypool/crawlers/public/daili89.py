from ProxyPool.crawlers.base import BaseCrawler

MAX_PAGE = 80
BASE_URL = 'https://www.89ip.cn/index_{page}.html'


class DaiLi89Crawl(BaseCrawler):
    """
    89代理 https://www.89ip.cn
    如果不想获取器执行这个代理 可以设置：ignore = True
    """
    urls = [BASE_URL.format(page=page) for page in range(1, MAX_PAGE+1)]
    ignore = False

    def parse(self, response):
        trs = response.xpath('//table[@class="layui-table"]/tbody/tr')
        for tr in trs:
            ip = tr.xpath('.//td[1]/text()')[0].lstrip().rstrip()
            port = tr.xpath('.//td[2]/text()')[0].lstrip().rstrip()
            proxy = '{}:{}'.format(ip, port)
            #elite = False
            #https = False
            yield proxy
