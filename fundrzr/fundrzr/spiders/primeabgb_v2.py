import scrapy
from ..items import PrimeAbgbItem
import re


class PrimeAbgb(scrapy.Spider):
    name = 'primeabgb2'
    start_urls = [
        'https://www.primeabgb.com/buy-online-price-india/graphic-cards-gpu/?pa-_stock_status=instock',
    ]

    def parse(self, response, ):
        all_containers = response.css('.product-innfo')
        items = PrimeAbgbItem()
        for container in all_containers:
            category_type_dict = {
                'cpu-processor': 'CPU',
                'graphic-cards-gpu': 'GPU',
            }
            category_match_obj = re.search(r'-india/(\w+(-\w+)?(-\w+)?)', str(response.url))
            category = category_match_obj.group(1)
            category = category_type_dict[category]
            product_url = container.css('.short a::attr(href)').get()

            yield scrapy.Request(product_url, callback=self.parse_each_product_page, meta={'category': category, 'items': items})

        """bext page logic"""
        if not response.css('.next'):
            next_page = None
        else:
            next_page = response.css('.next::attr(href)').get()

        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_each_product_page(self, response):
        items = response.meta['items']
        product_name = response.css('.entry-title::text').get().strip().encode('ascii', 'ignore').decode("utf-8")
        price = response.css('.summary ins .amount::text').get()
        if not price:
            price = response.css('.summary .amount::text').get()
        price = self.process_price_string(str(price))
        brand = response.css('.woocommerce-product-attributes-item--attribute_pa_brand a::text').get().strip()
        category = response.meta['category']
        # model = re.search(r'\s(\w+((-\w+)?)*)$', product_name).group(1)
        model = response.css('.sku::text').get().strip()

        url = response.url
        items['product_name'] = product_name
        items['price'] = price
        items['brand'] = brand
        items['type'] = category
        items['url'] = url
        items['model'] = model

        yield items

    def process_price_string(self, price_str):
        ptns_to_remove = [r'[Rr][Ss]\.', r',']
        for ptn in ptns_to_remove:
            price_str = re.sub(ptn, '', price_str)
        price_str = price_str.encode('ascii', 'ignore').decode("utf-8").strip()
        return float(price_str)
