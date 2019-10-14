import scrapy
from ..items import MdcomputersItem
import re


class Mdcmpv2(scrapy.Spider):
    name = 'mdcomputers2'
    start_urls = [
        'https://mdcomputers.in/graphics-card',
    ]

    def parse(self, response):
        items = MdcomputersItem()
        all_containers = response.css('.right-b')
        for container in all_containers:
            product_url = container.css('h4 a::attr(href)').get()
            category_type_dict = {
                'processor': 'CPU',
                'graphics-card': 'GPU',
            }
            category_match_obj = re.search(r'\.in\/(\w+(-)?(\w+)?)(.html)?', response.url)
            category = category_match_obj.group(1)
            category = category_type_dict[category]

            yield scrapy.Request(product_url, callback=self.parse_each_product_page, meta={'category': category, 'items': items})

        """next page logic"""
        if response.css('.pagination>li:nth-last-child(2)>a::text').get() != '>':
            next_page = None
        else:
            next_page = response.css('.pagination>li:nth-last-child(2)>a::attr(href)').get()
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_each_product_page(self, response):
        items = response.meta['items']
        product_name = response.css('h1::text').get().strip().encode('ascii', 'ignore').decode("utf-8")
        price = response.css('.price-new>span::text').get()
        price = self.process_price_string(price)
        brand = response.css('.brand>a>span::text').get().strip()
        model = response.css('.model::text').get().strip()
        category = response.meta['category']
        url = response.url
        items['product_name'] = product_name
        items['price'] = price
        items['brand'] = brand
        items['model'] = model
        items['type'] = category
        items['url'] = url

        yield items

    def process_price_string(self, price_str):
        ptns_to_remove = [r'[Rr][Ss]\.', r',']
        for ptn in ptns_to_remove:
            price_str = re.sub(ptn, '', price_str)
        price_str = price_str.encode('ascii', 'ignore').decode("utf-8").strip()
        return float(price_str)
