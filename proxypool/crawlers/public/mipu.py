from ProxyPool.crawlers.base import BaseCrawler

PROXY_TYPE = ['in_tp', 'in_hp']
BASE_URL = 'https://proxy.mimvp.com/freeopen?proxy={stype}'


class MiPuCrawl(BaseCrawler):
    """
    米扑 https://proxy.mimvp.com
    如果不想获取器执行这个代理 可以设置：ignore = True
    """
    urls = [BASE_URL.format(stype=stype) for stype in PROXY_TYPE]
    ignore = False

    def parse(self, response):
        port_img_map = {'DMxMjg': '3128', 'Dgw': '80', 'DgwODA': '8080',
                        'DgwOA': '808', 'DgwMDA': '8000', 'Dg4ODg': '8888',
                        'DgwODE': '8081', 'Dk5OTk': '9999', 'DQyMDU1': '42055',
                        'DU1NDQz': '55443', 'DgwMDE': '8001', 'DExMA': '110',
                        'DUzMjgx': '53281', 'DEwMDAw': '10000', 'Dgx': '82',
                        'Dgy': '82', 'DMxMjk': '3129'}
        trs = response.xpath('//table[@class="mimvp-tbl free-proxylist-tbl"]/tbody/tr')
        for tr in trs:
            ip = tr.xpath('.//td[2]/text()')[0]
            port_img = tr.xpath('./td[3]/img/@src')[0].split('port=')[1]
            port = port_img_map.get(port_img[14:].replace('O0O', ''))
            #elite = '高匿' in tr.xpath('.//td[5]/text()').get()
            #https = 'HTTPS' in tr.xpath('.//td[4]/text()').get()
            if port is not None:
                proxy = '{}:{}'.format(ip, port)
                yield proxy