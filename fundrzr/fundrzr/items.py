# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MdcomputersItem(scrapy.Item):
    product_name = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    type = scrapy.Field()
    brand = scrapy.Field()
    model = scrapy.Field()


class TheItDepotItem(scrapy.Item):
    product_name = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    type = scrapy.Field()
    brand = scrapy.Field()
    model = scrapy.Field()


class PrimeAbgbItem(scrapy.Item):
    product_name = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    type = scrapy.Field()
    brand = scrapy.Field()
    model = scrapy.Field()


class VedantcItem(scrapy.Item):
    product_name = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    type = scrapy.Field()
    brand = scrapy.Field()
    model = scrapy.Field()


class PhdEssaysItem(scrapy.Item):
    essay_title = scrapy.Field()
    essay_url = scrapy.Field()


class TechpowerUpItem(scrapy.Item):
    series_name = scrapy.Field()
    product_name = scrapy.Field()
    vram = scrapy.Field()
    model = scrapy.Field()
    boost_clock = scrapy.Field()
    base_clock = scrapy.Field()
    type = scrapy.Field()
    brand = scrapy.Field()

class Gpuzoo(scrapy.Item):
    series_name = scrapy.Field()
    product_name = scrapy.Field()
    vram = scrapy.Field()
    model = scrapy.Field()
    boost_clock = scrapy.Field()
    base_clock = scrapy.Field()
    type = scrapy.Field()
    brand = scrapy.Field()
