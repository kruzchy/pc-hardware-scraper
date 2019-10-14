import scrapy
import re
from ..items import TechpowerUpItem

class TechPowerUp(scrapy.Spider):
    name = 'gpu-tech'
    base_link = 'https://www.techpowerup.com'
    start_urls = [
        'https://www.techpowerup.com/gpu-specs/?mfgr=NVIDIA&mobile=No&igp=No&sort=name',
    ]

    def parse(self, response):
        list_years = [option.attrib['value'] for option in response.css('#released>option')[1:]]
        links_by_year = [response.url+f'&released={year}' for year in list_years]
        for year_link in links_by_year:
            print(f'Year: {year_link}')
            yield scrapy.Request(year_link, callback=self.parse_each_year)

    def parse_each_year(self, response):
        all_containers = response.css('.processors>tr>td:first-child>a')
        for container in all_containers:
            series_link = self.base_link + container.attrib['href']
            yield scrapy.Request(series_link, callback=self.parse_each_series)

    def parse_each_series(self, response):
        series_name = response.css('.gpudb-name::text').get()
        all_containers = response.css('#boards>table>tbody>tr')
        if not all_containers:
            print(f'>>Reference/No variants for this card')
            yield scrapy.Request(response.url, callback=self.parse_each_product, meta={'series_name': series_name, 'base_clock': None, 'boost_clock': None})
            return

        for container in all_containers:
            product_link = self.base_link+container.css('.has-image>a::attr(href)').get()
            base_clock = container.css('td:nth-child(2)::text').get()
            boost_clock = container.css('td:nth-child(3)::text').get()
            yield scrapy.Request(product_link, callback=self.parse_each_product, meta={'series_name': series_name, 'base_clock': base_clock, 'boost_clock': boost_clock})

    def parse_each_product(self, response):
        items = TechpowerUpItem()
        series_name = response.meta['series_name']
        product_name = response.css('.gpudb-name::text').get()
        vram = response.css(".gpudb-specs-large__entry:nth-child(5) .gpudb-specs-large__value::text").get()
        model = response.css(".gpudb-name__partnum::text").get()
        boost_clock = response.meta['boost_clock']
        base_clock = response.meta['base_clock']
        type = 'GPU'
        brand = product_name.split(' ')[0]
        items['series_name'] = series_name
        items['product_name'] = product_name
        items['vram'] = vram
        items['model'] = model
        items['boost_clock'] = boost_clock
        items['base_clock'] = base_clock
        items['type'] = type
        items['brand'] = brand
        yield items