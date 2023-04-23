import scrapy
from scrapy.spiders import CrawlSpider,  Rule
from scrapy.linkextractors import LinkExtractor


class MySpiderForPlayers(CrawlSpider):
    user_agent ="Custom"
    name = "fbref"
    allowed_domains = ["fbref.com"]
    start_urls =  ['https://fbref.com/en/players/']
    custom_settings = {
        "DOWNLOAD_DELAY" : 4,
        "DOWNLOAD_TIMEOUT" : 9,
        "CONCURRENT_REQUESTS" : 20,
        'FEEDS': {
            '%(name)s.csv': {
                'format': 'csv',
                'overwrite': True
            }
        }
    }    
    
    rules = (
    #    Rule(LinkExtractor(allow = r'profil\/spieler'), callback='parse_players', follow=True)
        Rule(LinkExtractor(allow = r'\/players\/([a-z]+)',
                           restrict_xpaths=('//*[@class="section_wrapper"]')
                           ), 
            callback='parse_club_links', follow=False),
     #   Rule(LinkExtractor(allow = r'profil\/spieler'), callback='parse_players', follow=True)
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
        #     print(count)
        #     count += 1
        #     if count >= 100 :
        #         break
        #    if "/profil/spieler/" in title:    
           #     print( title )
    #            yield( {"title": title} )    
               # yield scrapy.Request(response.urljoin(title), callback=self.parse_players, headers={'User-Agent': 'Custom'})
       #     else:
            yield {"url": link.text, "text": link.url}
    