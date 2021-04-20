import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from joblistingscraper.items import JoblistingItem


class indeedNL(CrawlSpider):
    name = 'indeedNL'
    allowed_domains = ['nl.indeed.com']
    start_urls = ['https://nl.indeed.com/developer-vacatures']
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="pagination-list"]/li/a')),
        Rule(LinkExtractor(restrict_xpaths='//h2[@class="title"]/a'), callback='parse_book'),
    )

    def parse_book(self, response):
        loader = ItemLoader(item=JoblistingItem(), response=response)
        loader.add_xpath('title', '//h1/text()')
        loader.add_xpath('description', '//div[@id="jobDescriptionText"]')
        yield loader.load_item()
