import scrapy


class ScrapeStats(scrapy.Spider):
    name = 'fights'


    def start_requests(self):
        urls = [
            'http://www.ufcstats.com/statistics/events/completed?page=all'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        title = response.css('title::text').get()
        yield {'site_title': title}



