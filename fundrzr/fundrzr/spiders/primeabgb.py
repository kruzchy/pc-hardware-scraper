import scrapy
from ..items import PrimeAbgbItem
import re


class PrimeAbgb(scrapy.Spider):
    name = 'primeabgb'
    start_urls = [
        'https://www.primeabgb.com/buy-online-price-india/cpu-processor/page/1/?pa-_stock_status=instock',
    ]

    def parse(self, response, ):
        all_containers = response.css('.product-innfo')
        items = PrimeAbgbItem()
        for container in all_containers:
            product_name = container.css('.short a::text').get().strip().encode('ascii', 'ignore').decode("utf-8")
            price = container.css('#main .amount::text').get()
            price = self.process_price_string(str(price))
            brand = re.search(r'^\w+', product_name).group(0)
            category_type_dict = {
                'cpu-processor': 'CPU',
                'graphic-cards-gpu': 'GPU',
            }
            category_match_obj = re.search(r'-india/(\w+(-\w+)?)', str(response.url))
            category = category_match_obj.group(1)
            category = category_type_dict[category]
            url = container.css('.short a::attr(href)').get()
            items['product_name'] = product_name
            items['price'] = price
            items['brand'] = brand
            items['type'] = category
            items['url'] = url

            yield items

        if not response.css('.next'):
            next_page = None
        else:
            next_page = response.css('.next::attr(href)').get()

        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)

    def process_price_string(self, price_str):
        ptns_to_remove = [r'[Rr][Ss]\.', r',']
        for ptn in ptns_to_remove:
            price_str = re.sub(ptn, '', price_str)
        price_str = price_str.encode('ascii', 'ignore').decode("utf-8").strip()
        return int(price_str)
