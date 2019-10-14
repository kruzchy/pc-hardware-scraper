import scrapy
from ..items import TheItDepotItem
import re
from urllib.parse import quote,unquote

class TheItDepot(scrapy.Spider):
    name = 'theitdepot'
    start_urls = [
        'https://www.theitdepot.com/products-Processors_C30.html',
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
        for page in range(1, int(max_pages)+1):
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
            yield scrapy.FormRequest('https://www.theitdepot.com/category_filter.php', formdata=data, callback=self.parse_each_page, meta={'category_name': category_type_dict[category_name]})

    def parse_each_page(self, response):
        category_name = response.meta['category_name']
        all_containers = response.css('.tab-pane')[1].css('.product-info')
        items = TheItDepotItem()
        for container in all_containers:
            """skip container if out of stock"""
            if container.css('.outStock'):
                continue
                
            product_name = container.css('.name a::text').get().strip().encode('ascii', 'ignore').decode("utf-8")
            price = container.css('.price::text').get()
            price = self.process_price_string(price)
            url = container.css('.name a::attr(href)').get()
            brand_match_obj = re.search(r'Brand : (\w+)', container.css('.description::text').get().strip())
            if brand_match_obj:
                brand = re.search(r'Brand : (\w+)', container.css('.description::text').get().strip()).group(1)
            else:
                brand = product_name.split(' ')[0]
            items['product_name'] = product_name
            items['price'] = price
            base_link = 'https://www.theitdepot.com/'
            items['url'] = base_link+url
            items['type'] = category_name
            items['brand'] = brand
            yield items


    def process_price_string(self, price_str):
        ptns_to_remove = [r'[Rr][Ss]\.', r',']
        for ptn in ptns_to_remove:
            price_str = re.sub(ptn, '', price_str)
        price_str = price_str.encode('ascii', 'ignore').decode("utf-8").strip()
        return int(price_str)
