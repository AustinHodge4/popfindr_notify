import argparse
import time

import lxml.html as lh
import pandas as pd
import requests
from notify_run import Notify

cached = []
def main(url, notify):
    global cached
    page = requests.get(url)
    doc = lh.fromstring(page.content)
    tr_elements = doc.xpath('//table[2]/tbody/tr/th[3]/text()')
    # print(page.content)
    # print(tr_elements)
    count = tr_elements
    count = [x for x in count if x != '0']
    if count:
        if cached == count: 
            return
        notify.send(f"Xbox Series X in Stock! {count}", url)
        print(f"Xbox Series X in Stock! {count}")
        cached = count
    # print("None found")

def start():
    my_parser = argparse.ArgumentParser(description='Queries Xbox Series X stock for nearby Targets using popfindr site')
    my_parser.add_argument('--url', '-u',
                       type=str,
                       required=True,
                       help='popfindr request url')
    my_parser.add_argument('--notify', '-n',
                       metavar='notify_endpoint',
                       type=str,
                       required=True,
                       help='notify.run push endpoint')
    
    args = my_parser.parse_args()
    print(f"Notify endpoint: {args.notify}")
    notify = Notify(endpoint=str(args.notify))

    while True:
        main(args.url, notify)
        time.sleep(0.5)

start()
