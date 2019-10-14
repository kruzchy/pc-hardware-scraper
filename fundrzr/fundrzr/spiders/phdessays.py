import scrapy
from ..items import PhdEssaysItem


class PhdessaysSpider(scrapy.Spider):
    name = 'phdessays'
    start_urls = ['https://phdessay.com/free-essays/']

    def parse(self, response):
        max_pages = response.css('.paginate li:last-child a::text').get().replace(',', '')
        for page_num in range(1, 4):
            current_url = f'https://phdessay.com/free-essays/page/{page_num}/'
            self.start_urls.append(current_url)
            yield scrapy.Request(current_url, callback=self.parse_essay_links)

    def parse_essay_links(self, response):
        all_essay_urls = response.css('.phdessay-card-read::attr(href)').getall()
        for essay_url in all_essay_urls:
            yield scrapy.Request(essay_url, callback=self.parse_essay_contents)

    def parse_essay_contents(self, response):
        items = PhdEssaysItem()
        essay_title = response.css('.site-title::text').get()
        essay_url = response.request.url
        items['essay_title'] = essay_title
        items['essay_url'] = essay_url
        yield items
