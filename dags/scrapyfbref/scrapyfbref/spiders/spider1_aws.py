import scrapy
from scrapy.spiders import CrawlSpider,  Rule
from scrapy.linkextractors import LinkExtractor
import boto3

class MySpiderForPlayers(CrawlSpider):
    user_agent ="Custom"
    name = "fbref"
    allowed_domains = ["fbref.com"]
    start_urls =  ['https://fbref.com/en/players/']
    custom_settings = {
        "DOWNLOAD_DELAY" : 4,
        "DOWNLOAD_TIMEOUT" : 9,
        "CONCURRENT_REQUESTS" : 20,
#         "FEEDS" : {
#             's3://fbrefdata0921/players_links.csv': {
#                 'format': 'csv',
#                 'encoding': 'utf8',
#                 'store_empty': False
#     }
# }
    }    
    
    rules = (
        Rule(LinkExtractor(allow = r'\/players\/([a-z]+)',
                           restrict_xpaths=('//*[@class="section_wrapper"]')
                           ), 
            callback='parse_club_links', follow=False),
    )
    
    

    def parse_club_links(self, response):
        count = 0 
        link_extractor = LinkExtractor(allow = r'\/players\/([a-z0-9]+)\/([A-z]+)',
                                       restrict_xpaths='//*[@class="section_wrapper"]',
                                        deny = r"\/players\/([a-z0-9]+)\/([A-z]+)\/\d+"
                                       )
        club_links = link_extractor.extract_links(response)
        print(response.url)
        attributes = {}
        count = 0 

        for link in club_links :
            yield {"url": link.text, "text": link.url}
    
