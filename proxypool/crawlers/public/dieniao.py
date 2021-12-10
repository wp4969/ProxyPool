from proxypool.crawlers.base import BaseCrawler

MAX_PAGE = 6
BASE_URL = 'https://www.dieniao.com/FreeProxy/{page}.html'


class DieNiaoCrawl(BaseCrawler):
    """
    蝶鸟代理 https://www.dieniao.com
    如果不想获取器执行这个代理 可以设置：ignore = True
    """
    urls = [BASE_URL.format(page=page) for page in range(1, MAX_PAGE+1)]
    ignore = False

    def parse(self, response):
        lis = response.xpath('//li[@class="f-list col-lg-12 col-md-12 col-sm-12 col-xs-12"]')
        for li in lis:
            ip = li.xpath('.//span[1]/text()')[0]
            port = li.xpath('.//span[2]/text()')[0]
            proxy = '{}:{}'.format(ip, port)
            #elite = '高匿' in li.xpath('.//span[3]/text()').get()
            #https = False
            yield proxy
