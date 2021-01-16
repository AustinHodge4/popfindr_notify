import argparse
import time

from notify_run import Notify

from checkers.nowinstock import NowInStockChecker
from checkers.popfindr import PopfindrChecker

popfindr_url_format = 'https://popfindr.com/results?pid=207-41-0001&zip={}&range=50&webpage=target&token=03AGdBq26iPvIDpBhjblp9ch5Vz0MElvac1VOZdGIr3QbQm2ALnDkRqf18nViHGPY1iaz7ZKakUtKs91CemxEvIz6X1H52VssYW8puc1c0hipu-aHN1YVdeqYiJd3mSljTNYKlWu4aOsPkYDwhuKo01HaaaCSeIS4Jy5EKtMG2iGdxKk06b1U92PUbIU6S6fSGsFCrCFOv7kLP8wNOU6CFouJZvm_0IEL86by89UG8TPjCU7jxfEknxD3j65aPOgFsUmP6q89RUSWCPCGPv-_fdeWtXLJoHYUBdEZ6U9Y3jAGXUk90s9XRgdBvWneEyrBhr5jfRg_u1W6wUswfLQ0uScBHHcTzDi4c-1i_xrOv2RcMRvgIdnhkseAzsPibj7oqAYLvIC6Wx_kTj_7JUJRZlmYjcKhXyNDyQqIZ00vX9Td0RcAxygCPZUF2Z5UgX3AHY38BoekJjphWzMqF4SlV8FxWPkbI3B3WYVk6DLayBolANUkk2hBH80TpqILuJtvsc8qUlGwjNYtg'

DESCRIPTION = '''
Simple python script to notify when a product is in stock.
Checks every 45 seconds.
Supports popfindr and nowinstock products.
For popfindr, it will notify which stores near you currently has some in stock.
When using nowinstock, the product only matches if the value is in the name on the site so it may not pick up all products.

Note: Popfindr doesn't work atm. :(
'''
EXAMPLE_USAGE = '''
examples:

python main.py -t popfindr -u "https://popfindr.com/results?pid=207-..." -n "https://notify.run/auN2NjQ1mRcH27vy"
python main.py -t popfindr -z 27110 -n "https://notify.run/auN2NjQ1mRcH27vy"
python main.py -t nowinstock -p "RYZEN 9 5900x" -u "https://www.nowinstock.net/computers/processors/amd/" -n "https://notify.run/auN2NjQ1mRcH27vy"

NOTE: urls and values with spaces are quoted
'''
def start():

    my_parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        epilog=EXAMPLE_USAGE,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    group = my_parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--url', '-u',
                       type=str,
                       help='stock website request url')
    my_parser.add_argument('--type', '-t',
                       metavar='resource_type',
                       type=str.lower,
                       required=True,
                       choices=['nowinstock', 'popfindr'],
                       help='the resource url type')
    my_parser.add_argument('--product', '-p',
                       metavar='name',
                       type=str,
                       help='the product to look for. This only works for the nowinstock type. ie. RYZEN 9 5900x')
    group.add_argument('--zipcode', '-z',
                       type=str,
                       help='zipcode to search Xbox Series X for (only for popfindr)')
    my_parser.add_argument('--notify', '-n',
                       metavar='notify_endpoint',
                       type=str,
                       required=True,
                       help='notify.run push endpoint')
    
    args = my_parser.parse_args()

    if not bool(args.zipcode) ^ bool(args.type == 'nowinstock'):
        my_parser.error('--zipcode and --type [nowinstock] cannot be given together')
    
    if bool(args.product) ^ bool(args.type == 'nowinstock'):
        my_parser.error('--product and --type [nowinstock] must be given together')

    if not args.url:
        url = popfindr_url_format.format(args.zipcode)
    else:
        url = args.url

    print(f"Notify endpoint: {args.notify}")
    notify = Notify(endpoint=str(args.notify))

    stock_checker = None

    if args.type == 'popfindr':
        print(f"\nPopfindr page: {url}\n")
        stock_checker = PopfindrChecker(url, notify)
    elif args.type == 'nowinstock':
        print(f"\nNowInStock page: {url}\n")
        stock_checker = NowInStockChecker(url, notify, args.product)
        # stock_checker.run()

    
    if stock_checker:
        while True:
            stock_checker.run()
            time.sleep(45)

start()
