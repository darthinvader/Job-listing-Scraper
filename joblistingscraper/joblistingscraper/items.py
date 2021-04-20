# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from bs4 import BeautifulSoup
from itemloaders.processors import MapCompose
from w3lib.html import remove_tags


class JoblistingItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field(
        input_processor=MapCompose(remove_tags)
    )
