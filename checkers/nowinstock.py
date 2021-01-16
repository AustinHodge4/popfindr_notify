from checkers.stock_checker_base import StockChecker


class NowInStockChecker(StockChecker):

    def __init__(self, url, notify, product):
        super().__init__(url, notify)
        self.product = product
        self.cache = {}     
        self.status_order = ['In Stock', 'Preorder', 'Out of Stock']

    def run(self):
        doc = self.fetch_html()
        # print(doc.prettify())
        items = doc.select('div[id=data]')[0].select('table tr')[1:-1]
        in_stock = []
        for item in items:
            name = item.select('td a')[0].get_text()
            if self.product.lower() in name.lower():
                status = item.select('td')[1].get_text()
                price = item.select('td')[2].get_text()
                updated_at = item.select('td')[3].get_text()
                product_link = item.select('td a')[0]['href']
                # print(f'\n{name}, {status}, {price}, {updated_at}, {product_link}')
                
                if not name in self.cache or status != self.cache[name]['status']:
                    meta_data = {'name': name, 'status': status, 'price': price, 'link': product_link, 'updated_at': updated_at if updated_at != '-' else None}
                    if not status in ['Out of Stock', 'Not Tracking']:
                        print(f"{name} at {price} is in stock! {product_link}\n")
                        in_stock.append(meta_data)
                    self.cache[name] = meta_data

        if in_stock:
            # This will many notifications but only one will actually show. so, we sort by lowest price then by status 
            # to choose what product link to go to when the notification is clicked
            sorted_data = sorted(in_stock, key=lambda k: (k['price'], self.status_order.index(k['status'])), reverse=True)
            for item in sorted_data:
                # print(item)
                self.send_push(f"{item['name']} at {item['price']} is in stock! {item['link']}", action=item['link'])

