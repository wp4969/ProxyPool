from ProxyPool.crawlers.base import BaseCrawler

PROXY_TYPE = range(1, 34)
BASE_URL = 'http://www.66ip.cn/areaindex_{stype}/1.html'


class DaiLi66Crawl(BaseCrawler):
    """
    66代理 http://www.66ip.cn
    如果不想获取器执行这个代理 可以设置：ignore = True
    """
    urls = [BASE_URL.format(stype=stype) for stype in PROXY_TYPE]
    ignore = False

    def parse(self, response):
        trs = response.xpath('//div[@class="footer"]/div/table/tr[position() > 1]')
        for tr in trs:
            ip = tr.xpath('.//td[1]/text()')[0]
            port = tr.xpath('.//td[2]/text()')[0]
            proxy = '{}:{}'.format(ip, port)
            #elite = '高匿' in tr.xpath('.//td[4]/text()').get()
            #https = False
            yield proxy
