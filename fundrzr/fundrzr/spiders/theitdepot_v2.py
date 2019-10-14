import scrapy
from ..items import TheItDepotItem
import re
from urllib.parse import quote, unquote


class TheItDepot(scrapy.Spider):
    name = 'theitdepot2'
    start_urls = [
        'https://www.theitdepot.com/products-Graphic+Cards_C45.html'
    ]

    def parse(self, response):
        match_obj = re.search(r'/products-(.+)_C(\d+).html', response.url)
        category_name = match_obj.group(1).replace('+', ' ')
        category_id = match_obj.group(2)
        category_type_dict = {'Processors': 'CPU',
                              'Graphic Cards': 'GPU'

                              }
        max_pages = response.css('.pagination-container>ul>li:last-child>a::attr(id)').get()
        for page in range(1, int(max_pages) + 1):
            data = {
                'categoryname': category_name,
                'filter-limit': '12',
                'filter-orderby': 'price_asc',
                'filter_listby': 'Grid',
                'category': category_id,
                'pageno': str(page),
                'total_pages': str(max_pages),
                'PageScrollProcess': 'No',
                'PageFinished': 'No',
                'filter': 'true'
            }
            yield scrapy.FormRequest('https://www.theitdepot.com/category_filter.php', formdata=data,
                                     callback=self.parse_each_page,
                                     meta={'category_name': category_type_dict[category_name]})

    def parse_each_page(self, response):
        category_name = response.meta['category_name']
        all_containers = response.css('.tab-pane')[1].css('.product-info')
        items = TheItDepotItem()
        for container in all_containers:
            """skip container if out of stock"""
            if container.css('.outStock'):
                continue

            base_link = 'https://www.theitdepot.com/'
            product_url = container.css('.name a::attr(href)').get()
            product_url = base_link + product_url

            yield scrapy.Request(product_url, callback=self.parse_each_product_page, meta={'items': items, 'category': category_name})


    def parse_each_product_page(self, response):
        items = response.meta['items']
        product_name =  response.css(".singleprodutTop .name::text").get().strip().encode('ascii', 'ignore').decode("utf-8")
        price = response.css(".price-box .price::text").get()
        price = self.process_price_string(price)
        category = response.meta['category']
        brand = response.css("tr:nth-child(2) td+ td::text").get().strip()
        model = response.css("tr:nth-child(3) td+ td::text").get().strip()
        url = response.url

        items['product_name'] = product_name
        items['price'] = price
        items['brand'] = brand
        items['model'] = model
        items['type'] = category
        items['url'] = url

        yield items

    def process_price_string(self, price_str):
        ptns_to_remove = [r'[Rr][Ss](\.)?', r',', r'/-']
        for ptn in ptns_to_remove:
            price_str = re.sub(ptn, '', price_str)
        price_str = price_str.encode('ascii', 'ignore').decode("utf-8").strip()
        return float(price_str)
