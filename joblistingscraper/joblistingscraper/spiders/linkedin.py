from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from joblistingscraper.items import JoblistingItem

base_urls = [
    'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=$job&location=Amsterdam&geoId=&trk=homepage-jobseeker_jobs-search-bar_search-submit&start=$page']

developers_key_words = ['developer', 'web developer', 'programmer', 'software engineer', 'software developer']


def linkedInApiUrls():
    urls = []
    for url in base_urls:
        for key_word in developers_key_words:
            for i in range(0, 1000, 20):
                new_url = url.replace('$page', str(i))
                new_url = new_url.replace('$job', key_word)
                urls.append(new_url)
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
