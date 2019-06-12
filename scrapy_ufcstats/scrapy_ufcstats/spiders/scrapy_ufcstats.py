import scrapy
import unicodedata

class ScrapeStats(scrapy.Spider):
    name = 'fights'


    def start_requests(self):
        urls = [
            'http://www.ufcstats.com/statistics/events/completed?page=all'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # Step #1: Fetch all event urls
    def parse(self, response):
        for event_url in response.css('.b-link_style_black::attr(href)').getall():
            yield scrapy.Request(event_url, callback=self.parse_event)

    # Step #2: Fetch all fight urls from each event
    def parse_event(self, response):
        for fight_url in response.css('a.b-flag_style_green::attr(href)').getall():
            fight_url = unicodedata.normalize('NFKD', fight_url).encode('ascii', 'ignore')
            yield {'fight_url': fight_url}




