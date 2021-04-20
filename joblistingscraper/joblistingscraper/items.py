# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from bs4 import BeautifulSoup
from scrapy.loader.processors import MapCompose
from w3lib.html import remove_tags

class JoblistingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field(
        input_processor = MapCompose(remove_tags)
    )
