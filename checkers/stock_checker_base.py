import time

import requests
from bs4 import BeautifulSoup


class StockChecker():

    def __init__(self, url, notify):
        self.notify = notify
        self.url = url
        self.session = None

    def run(self):
        raise NotImplementedError('Need to implement run method')

    def fetch_html(self):
        if not self.session:
            self.session = requests.Session()

        page = self.session.get(self.url, timeout=2)
        return BeautifulSoup(page.content, 'html.parser')

    def send_push(self, message, action=None):
        self.notify.send(message, action)
    
