# ProxyPool

自用代理池，在崔庆才代理池的基础上修改的。大体框架无变化，改了一些符合自己习惯和熟悉的东西。

原地址：https://github.com/Python3WebSpider/ProxyPool

## 安装

需要如下环境：

* Docker
* Docker-Compose

安装方法自行搜索即可。

## 运行

如果安装好了 Docker 和 Docker-Compose，只需要一条命令即可运行。

```shell script
docker-compose up
```

## 可配置项

```python
###getter获取模块相关
PROXY_NUMBER_MAX：代理池最大数量

###tester测试模块相关
TEST_URL：代理池URL
TEST_BATCH：批量测试数量
TEST_TIMEOUT：请求超时时间
TEST_ANONYMOUS：是否开启高匿代理筛选
TEST_VALID_STATUS：成功响应码

###redis存储模块相关
REDIS_HOST：redis连接的地址
REDIS_PORT：redis连接的端口
REDIS_DB：redis连接的db
REDIS_KEY：redis连接的key
MIN_SCORE：最小分数
MAX_SCORE：最大分数
AMOUNT_SCORE：每次执行累加的值 -1为每次执行分数减1

###server接口模块相关
API_HOST：api地址
API_PORT：api端口
API_THREADED：是否开启flask多线程

###scheduler调度模块相关
TESTER_ENABLED：测试模块相关
GETTER_ENABLED：存储模块相关
SERVER_ENABLED：接口模块开关
TESTER_CYCLE：测试调度间隔时间
GETTER_CYCLE：存储调度间隔时间

###日志相关
LOGGER_ENABLED：是否开启日志记录
LOGGER_FILE：日志文件目录
LOGGER_LEVEL：日志记录级别
LOGGER_FORMAT：日志记录格式
LOGGER_ROTATION：日志文件分割规则 比如：'10 MB' or '00:00' or '1 week'
LOGGER_RETENTION：日志最长保留时间
```

## 扩展代理爬虫

新增一个类继承BaseCrawler，页面处理写在parse方法中，参数response是html对象

```python
from proxypool.crawlers.base import BaseCrawler

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

```

## LICENSE

MIT
