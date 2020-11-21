import argparse
import time

import lxml.html as lh
import pandas as pd
import requests
from notify_run import Notify

cached = []
popfindr_url_format = 'https://popfindr.com/results?pid=207-41-0001&zip={}&range=25&webpage=target&token=03AGdBq24QxTwt4sgHWYLG3eQc1Dpf0Z8CxfQtCyzVkgcLsJcU7dDnOy2qNR-kh-YOUNPRZrSTQVoRZh8kRdkCSSn4nl8ekXZ2Lr8yMKMWspnLP8s0XeGKB5QWV4v2ODcVpGqotiak-0y7Pd8CgrY0FKElbLK29KiMJoC9VyMX1-KrbvLxD0cBtsibrx6mYcr9kDBCKCjOmv10As77rVQZbzkgoC8ojNWSgcEH_GIvqg6QVBHvhHUrqeDx15TwFwyLBevBRr0DUhi85sVN6Ae4yMrLo4XS_UCISektJpF-3wwBlgRWqwOPh9S-J3J4Yq55357PF42xIMAQNZsroJIsENhSY3HvE046atMrHvZtA23YPKxQfFfIAKayu0S2whl7MMv9RZ8JaiDnEOMyZX37xsqDwspJs66QEUkDhTraefLQrLY9MPeJDEiGh9O7jJgR2oRjI6bA5jKAml0Sx0BjlDaB-bh8N-eObxZk9WH5Ax7cHOMZHwLW2htrpql06TmS-GWd_8i9JKxL'
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
    group = my_parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--url', '-u',
                       type=str,
                       help='popfindr request url')
    group.add_argument('--zipcode', '-z',
                       type=str,
                       help='zipcode to search for')
    my_parser.add_argument('--notify', '-n',
                       metavar='notify_endpoint',
                       type=str,
                       required=True,
                       help='notify.run push endpoint')
    
    args = my_parser.parse_args()

    if not args.url:
        url = popfindr_url_format.format(args.zipcode)
    else:
        url = args.url

    print(f"Notify endpoint: {args.notify}")
    print(f"\nPopfindr page: {url}\n")
    notify = Notify(endpoint=str(args.notify))

    while True:
        main(url, notify)
        time.sleep(0.5)

start()
