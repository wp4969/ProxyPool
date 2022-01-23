from flask import Flask, g, request
from proxypool.components.redisclient import RedisClient
from proxypool.setting import API_HOST, API_PORT, API_THREADED

app = Flask(__name__)

"""
接口模块: 所有接口方法
"""


def get_conn():
    """
    get redis client object
    :return:
    """
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


@app.route('/')
def index():
    return '<h2>Welcome to Proxy Pool System</h2>'


@app.route('/get', methods=['GET'])
def get_proxy():
    redis = get_conn()
    return str(redis.random())


@app.route('/all', methods=['GET'])
def get_proxy_all():
    redis = get_conn()
    proxies = redis.all()
    proxies_string = ''
    for proxy in proxies:
        proxies_string += str(proxy) + '\n'
    return proxies_string


@app.route('/count', methods=['GET'])
def get_count():
    redis = get_conn()
    return redis.counts()


@app.route('/delete', methods=['GET'])
def delete():
    redis = get_conn()
    proxy = request.args["proxy"]
    redis.increment(proxy)
    return ''


if __name__ == '__main__':
    app.run(host=API_HOST, port=API_PORT, threaded=API_THREADED)


