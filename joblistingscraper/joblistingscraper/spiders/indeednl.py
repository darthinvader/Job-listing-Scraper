from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from joblistingscraper.items import JoblistingItem

developers_key_words = ['developer', 'web developer', 'programmer', 'software engineer', 'software developer']
locations = ['Amsterdam', 'Rotterdam', 'Utrech', 'Netherlands', 'The Hague', 'Eindhoven', 'Tilburg', 'Groningen',
             'Almere', 'Breda', 'Netherlands', 'Nijmegen']

programmerNL = 'https://nl.indeed.com/vacatures?q=web developer&l=rotterdam'


def get_all_start_urls():
    urls = []
    for key_word in developers_key_words:
        for location in locations:
            urls.append(f'https://nl.indeed.com/vacatures?q={key_word}&l={location}')
    return urls



class indeedNL(CrawlSpider):
    name = 'indeedNL'
    allowed_domains = ['nl.indeed.com']
    start_urls = get_all_start_urls()
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="pagination-list"]/li/a')),
        Rule(LinkExtractor(restrict_xpaths='//h2[@class="title"]/a'), callback='parse_job_listing'),
    )

    def parse_job_listing(self, response):
        loader = ItemLoader(item=JoblistingItem(), response=response)
        loader.add_xpath('title', '//h1/text()')
        loader.add_xpath('description', '//div[@id="jobDescriptionText"]')
        yield loader.load_item()
