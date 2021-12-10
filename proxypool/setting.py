from environs import Env
import os

env = Env()
env.read_env()
logger_path = os.path.dirname(__file__)


"""
getter获取模块相关

PROXY_NUMBER_MAX：代理池最大数量
"""
PROXY_NUMBER_MAX = 50000


"""
tester测试模块相关

TEST_URL：代理池URL
TEST_BATCH：批量测试数量
TEST_TIMEOUT：请求超时时间
TEST_ANONYMOUS：是否开启高匿代理筛选
TEST_VALID_STATUS：成功响应码
"""
TEST_URL = env.str('TEST_URL', 'http://www.baidu.com')
TEST_BATCH = env.int('TEST_BATCH', 20)
TEST_TIMEOUT = env.int('TEST_TIMEOUT', 15)
TEST_ANONYMOUS = True
TEST_VALID_STATUS = env.list('TEST_VALID_STATUS', [200, 206, 302])


"""
redis存储模块相关

REDIS_HOST：redis连接的地址
REDIS_PORT：redis连接的端口
REDIS_DB：redis连接的db
REDIS_KEY：redis连接的key
MIN_SCORE：最小分数
MAX_SCORE：最大分数
AMOUNT_SCORE：每次执行累加的值 -1为每次执行分数减1
"""
REDIS_HOST = env.str('REDIS_HOST', 'localhost')
REDIS_PORT = env.int('REDIS_PORT', 6379)
REDIS_DB = env.int('REDIS_DB', 0)
REDIS_KEY = env.str('REDIS_KEY', 'proxy:baidu')
MIN_SCORE = 0
MAX_SCORE = 100
AMOUNT_SCORE = -1


"""
server接口模块相关

API_HOST：api地址
API_PORT：api端口
API_THREADED：是否开启flask多线程
"""
API_HOST = '0.0.0.0'
API_PORT = 5000
API_THREADED = True


"""
scheduler调度模块相关

TESTER_ENABLED：测试模块相关
GETTER_ENABLED：存储模块相关
SERVER_ENABLED：接口模块开关
TESTER_CYCLE：测试调度间隔时间
GETTER_CYCLE：存储调度间隔时间
"""
TESTER_ENABLED = env.bool('TESTER_ENABLED', True)
GETTER_ENABLED = env.bool('GETTER_ENABLED', True)
SERVER_ENABLED = env.bool('SERVER_ENABLED', True)
TESTER_CYCLE = env.int('TESTER_CYCLE', 30)
GETTER_CYCLE = env.int('GETTER_CYCLE', 30)


"""
日志相关

LOGGER_ENABLED：是否开启日志记录
LOGGER_FILE：日志文件目录
LOGGER_LEVEL：日志记录级别
LOGGER_FORMAT：日志记录格式
LOGGER_ROTATION：日志文件分割规则 比如：'10 MB' or '00:00' or '1 week'
LOGGER_RETENTION：日志最长保留时间
"""
LOGGER_ENABLED = True
LOGGER_FILE = logger_path + '/logs/proxypool_{time:YYYY-MM-DD}.log'
LOGGER_LEVEL = 'ERROR'
LOGGER_FORMAT = '{time:YYYY-MM-DD HH:mm:ss} - {level} - {file} - {line} - {message}'
LOGGER_ROTATION = '00:00'
LOGGER_RETENTION = '10 days'
