from checkers.stock_checker_base import StockChecker


class PopfindrChecker(StockChecker):

    def __init__(self, url, notify):
        super().__init__(url, notify)
        self.cache = []
        

    def run(self):
        doc = self.fetch_html()
        # tr_elements = doc.xpath('//table[2]/tbody/tr/th[3]/text()')
        print(doc.prettify())
        print(doc.select('table')[2].select('tbody tr th')[3])
        # count = tr_elements
        # count = [x for x in count if x != '0']
        # if count:
        #     if self.cache == count: 
        #         return
            
        #     self.send_push(f"Xbox Series X in Stock! {count}", action=self.url)
        #     print(f"Xbox Series X in Stock! {count}")
        #     self.cache = count

