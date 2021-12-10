import time
import multiprocessing
from loguru import logger
from proxypool.components.getter import Getter
from proxypool.components.tester import Tester
from proxypool.components.server import app
from proxypool.setting import TESTER_ENABLED, GETTER_ENABLED, SERVER_ENABLED, TESTER_CYCLE, GETTER_CYCLE, API_HOST, \
    API_PORT, API_THREADED, LOGGER_ENABLED, LOGGER_FILE, LOGGER_LEVEL, LOGGER_FORMAT, LOGGER_ROTATION, LOGGER_RETENTION


tester_process, getter_process, server_process = None, None, None


class Scheduler:
    """
    调度模块
    """
    def run_getter(self, cycle=GETTER_CYCLE):
        """
        获取代理
        """
        getter = Getter()
        loop = 0
        while True:
            logger.debug(f'getter loop {loop} start...')
            getter.run()
            loop += 1
            time.sleep(cycle)

    def run_tester(self, cycle=TESTER_CYCLE):
        """
        测试代理
        """
        tester = Tester()
        loop = 0
        while True:
            logger.debug(f'tester loop {loop} start...')
            tester.run()
            loop += 1
            time.sleep(cycle)

    def run_server(self):
        """
        开启API接口
        """
        app.run(host=API_HOST, port=API_PORT, threaded=API_THREADED)

    def run(self):
        global tester_process, getter_process, server_process
        try:
            logger.info('starting proxypool...')
            if TESTER_ENABLED:
                tester_process = multiprocessing.Process(target=self.run_tester)
                logger.info(f'starting tester, pid {tester_process.pid}...')
                tester_process.start()

            if GETTER_ENABLED:
                getter_process = multiprocessing.Process(target=self.run_getter)
                logger.info(f'starting getter, pid{getter_process.pid}...')
                getter_process.start()

            if SERVER_ENABLED:
                server_process = multiprocessing.Process(target=self.run_server)
                logger.info(f'starting getter, pid{server_process.pid}...')
                server_process.start()

            if TESTER_ENABLED:
                tester_process.join()
            if GETTER_ENABLED:
                getter_process.join()
            if SERVER_ENABLED:
                server_process.join()
        except KeyboardInterrupt:
            logger.info('received keyboard interrupt signal')
            tester_process.terminate()
            getter_process.terminate()
            server_process.terminate()
        finally:
            if TESTER_ENABLED:
                tester_process.join()
            if GETTER_ENABLED:
                getter_process.join()
            if SERVER_ENABLED:
                server_process.join()
            logger.info(f'tester is {"alive" if tester_process.is_alive() else "dead"}')
            logger.info(f'getter is {"alive" if getter_process.is_alive() else "dead"}')
            logger.info(f'server is {"alive" if server_process.is_alive() else "dead"}')
            logger.info('proxys terminated')


if __name__ == '__main__':
    if LOGGER_ENABLED:
        logger.add(LOGGER_FILE, level=LOGGER_LEVEL, format=LOGGER_FORMAT, retention=LOGGER_RETENTION,
                   rotation=LOGGER_ROTATION)
    scheduler = Scheduler()
    scheduler.run()