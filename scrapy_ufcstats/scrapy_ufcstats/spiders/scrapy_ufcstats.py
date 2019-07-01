from scrapy import Spider, Request
from ..items import ScrapyUfcstatsItem


class ScrapeStats(Spider):
    name = 'fights'

    def start_requests(self):
        urls = [
            'http://www.ufcstats.com/statistics/events/completed?page=all'
        ]
        for url in urls:
            yield Request(url=url, callback=self.parse)

    # Step #1: Fetch all event urls
    def parse(self, response):
        for event_url in response.css('.b-link_style_black::attr(href)').getall():
            yield Request(event_url, callback=self.parse_event)

    # Step #2: Fetch all fight urls from each event
    def parse_event(self, response):
        for fight_url in response.css('a.b-flag_style_green::attr(href)').getall():
            yield Request(fight_url, callback=self.parse_fight)

    # Step #3: Fetch data from each fight
    def parse_fight(self, response):
        items = ScrapyUfcstatsItem()
        print(response.url)

        # Extract fighter name
        fighters = response.xpath("//h3[@class='b-fight-details__person-name']//a/text()").extract()
        if len(fighters) == 0:
            fighters = response.xpath("//h3[@class='b-fight-details__person-name']/span/text()").extract()

        # Extract fighter nicknames
        nicknames = response.xpath("//p[@class='b-fight-details__person-title']/text()").extract()

        # Data wrangling names
        fighter_1 = fighters[0]
        fighter_1_nn = nicknames[0].strip()
        fighter_2 = fighters[1]
        fighter_2_nn = nicknames[1].strip()

        # Extract winner
        fighter_1_outcome = response.xpath("//body[@class='b-page']/section[@class='b-statistics__section_details']"
                                            "/div[@class='l-page__container']/div[@class='b-fight-details']"
                                            "/div[@class='b-fight-details__persons clearfix']"
                                            "/div[1]/i/text()").extract()
        fighter_1_outcome = fighter_1_outcome[0].strip()
        if fighter_1_outcome == "W":
            winner = fighter_1
        else:
            winner = fighter_2

            # Itemize the extracted data
        items['fighter_1'] = fighter_1
        items['fighter_1_nn'] = fighter_1_nn
        items['fighter_2'] = fighter_2
        items['fighter_2_nn'] = fighter_2_nn
        items['winner'] = winner

        yield items
