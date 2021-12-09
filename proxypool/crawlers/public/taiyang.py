from proxypool.crawlers.base import BaseCrawler

MAX_PAGE = 4
BASE_URL = 'http://www.taiyanghttp.com/free/page{page}/'


class TaiYangCrawl(BaseCrawler):
    """
    太阳代理 http://www.taiyanghttp.com
    如果不想获取器执行这个代理 可以设置：ignore = True
    """
    urls = [BASE_URL.format(page=page) for page in range(1, MAX_PAGE+1)]
    ignore = False

    def parse(self, response):
        divs = response.xpath('//div[@class="tr ip_tr"]')
        for div in divs:
            ip = div.xpath('.//div[1]/text()')[0]
            port = div.xpath('.//div[2]/text()')[0]
            proxy = '{}:{}'.format(ip, port)
            #elite = '高匿' in div.xpath('.//node()')[16].get()
            #https = 'HTTPS' in div.xpath('.//div[6]/text()').get()
            yield proxy
