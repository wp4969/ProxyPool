from fake_useragent import UserAgent
import os


class Header:
    def get_header(self):
        path = os.path.dirname(__file__)
        ua = UserAgent(path=f'{path}/fake_useragent.json')
        headers = {
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'User-Agent': ua.random
        }
        return headers
