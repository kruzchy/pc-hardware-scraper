import scrapy
from ..items import MdcomputersItem
import re


class Mdcmp(scrapy.Spider):
    name = 'mdcomputers'
    start_urls = [
        'https://mdcomputers.in/processor',
        'https://mdcomputers.in/graphics-card',
    ]

    def parse(self, response):
        all_containers = response.css('.right-b')
        items = MdcomputersItem()
        for container in all_containers:
            product_name = container.css('h4 a::text').get().strip().encode('ascii', 'ignore').decode("utf-8")
            product_name = re.sub(r'\d+\w+\sGen\s', '', product_name)
            price = container.css('.price-new::text').get()
            price = self.process_price_string(price)
            brand = re.search(r'^\w+', product_name).group(0)
            category_type_dict = {
                'processor': 'CPU',
                'graphics-card': 'GPU',
            }
            category_match_obj = re.search(r'\.in\/(\w+(-)?(\w+)?)(.html)?', response.url)
            category = category_match_obj.group(1)
            category = category_type_dict[category]
            url = container.css('h4 a::attr(href)').get()
            items['product_name'] = product_name
            items['price'] = price
            items['brand'] = brand
            items['type'] = category
            items['url'] = url

            yield items

        if response.css('.pagination>li:nth-last-child(2)>a::text').get() != '>':
            next_page = None
        else:
            next_page = response.css('.pagination>li:nth-last-child(2)>a::attr(href)').get()

        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)

    def process_price_string(self, price_str):
        ptns_to_remove = [r'[Rr][Ss]\.', r',']
        for ptn in ptns_to_remove:
            price_str = re.sub(ptn, '', price_str)
        price_str = price_str.encode('ascii', 'ignore').decode("utf-8").strip()
        return int(price_str)
