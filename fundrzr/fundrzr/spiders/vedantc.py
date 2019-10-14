import scrapy
from ..items import VedantcItem
import re


class Vedantc(scrapy.Spider):
    name = 'vedantc'
    start_urls = [
        'https://www.vedantcomputers.com/products/processor#/availability=1/sort=p.sort_order/order=ASC/limit=100',
        'https://www.vedantcomputers.com/products/graphics-card#/availability=1/sort=p.sort_order/order=ASC/limit=100',
    ]

    def parse(self, response):
        all_containers = response.css('.caption')
        items = VedantcItem()
        for container in all_containers:
            product_name = container.css('name a::text').get().strip().encode('ascii', 'ignore').decode("utf-8")
            price = container.css('.price::text').get()
            price = self.process_price_string(price)
            brand = re.search(r'^\w+', product_name).group(0)
            category_type_dict = {
                'processor': 'CPU',
                'graphics-card': 'GPU',
            }
            cat = response.url.split('#/availability=1')[0]
            category_match_obj = re.search(r'.com/products/(.*)', cat)
            category = category_match_obj.group(1)
            category = category_type_dict[category]
            url = container.css('name a::attr(href)').get()
            items['product_name'] = product_name
            items['price'] = price
            items['brand'] = brand
            items['type'] = category
            items['url'] = url

            yield items

        # if response.css('.pagination>li:nth-last-child(2)>a::text').get() != '>':
        #     next_page = None
        # else:
        #     next_page = response.css('.pagination>li:nth-last-child(2)>a::attr(href)').get()
        #
        # if next_page is not None:
        #     yield scrapy.Request(next_page, callback=self.parse)

    def process_price_string(self, price_str):
        ptns_to_remove = [r'[Rr][Ss]\.', r',']
        price_str = price_str.strip()
        for ptn in ptns_to_remove:
            price_str = re.sub(ptn, '', price_str)
        price_str = price_str.encode('ascii', 'ignore').decode("utf-8")
        return int(price_str)
