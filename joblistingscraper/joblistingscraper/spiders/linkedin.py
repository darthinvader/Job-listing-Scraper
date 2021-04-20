from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from joblistingscraper.items import JoblistingItem

developers_key_words = ['developer', 'web developer', 'programmer', 'software engineer', 'software developer']
locations = ['Amsterdam', 'Rotterdam', 'Utrech', 'Netherlands', 'The Hague', 'Eindhoven', 'Tilburg', 'Groningen',
             'Almere', 'Breda', 'Netherlands', 'Nijmegen']

def linkedInApiUrls():
    urls = []
    for key_word in developers_key_words:
        for location in locations:
            for i in range(0, 1000, 25):
                urls.append(f'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={key_word}&location={location}&geoId=&trk=homepage-jobseeker_jobs-search-bar_search-submit&start={i}')
    return urls


class linkedin(CrawlSpider):
    name = 'linkedin'
    allowed_domains = ['linkedin.com']
    start_urls = linkedInApiUrls()
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//li/a'), callback='parse_job_listing'),
    )

    def parse_job_listing(self, response):
        loader = ItemLoader(item=JoblistingItem(), response=response)
        loader.add_xpath('title', '//h1[@class="topcard__title"]/text()')
        loader.add_xpath('description', '//section[@class="description"]')
        yield loader.load_item()
