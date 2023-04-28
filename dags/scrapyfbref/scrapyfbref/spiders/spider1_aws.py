import scrapy
from scrapy.spiders import CrawlSpider,  Rule
from scrapy.linkextractors import LinkExtractor
import boto3
import botocore.credentials

class MySpiderForPlayers(CrawlSpider):
    user_agent ="Custom"
    name = "fbref"
    allowed_domains = ["fbref.com"]
    start_urls =  ['https://fbref.com/en/players/']
    #start_urls = ["https://fbref.com/en/players/08f5afaa/Gianluigi-Donnarumma"]
    custom_settings = {
        "DOWNLOAD_DELAY" : 4,
        "DOWNLOAD_TIMEOUT" : 9,
        "CONCURRENT_REQUESTS" : 20,
        "CLOSESPIDER_TIMEOUT" : 60 * 5
    #    "CLOSESPIDER_PAGECOUNT" : 10,
  #      "CLOSESPIDER_ITEMCOUNT" : 100
#         "FEEDS" : {
#             's3://fbrefdata0921/players_links.csv': {
#                 'format': 'csv',
#                 'encoding': 'utf8',
#                 'store_empty': False
#     }
# }
    }    

#--------------------------SECTION 1-----------------------------------------------

    # def parse(self, response) : 
    #     link_extractor = LinkExtractor(allow = r'\/players\/([a-z]+)',
    #                        restrict_xpaths=('//*[@class="section_wrapper"]')
    #                        )
            
    #     club_links = link_extractor.extract_links(response)
    #     for link in club_links :
    #         yield scrapy.Request(link.url, callback=self.parse_club_links, headers={'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'})



    # def parse_club_links(self, response):
    #     count = 0 
    #     link_extractor = LinkExtractor(allow = r'\/players\/([a-z0-9]+)\/([A-z]+)',
    #                                    restrict_xpaths='//*[@class="section_wrapper"]',
    #                                     deny = [ r"\/players\/([a-z0-9]+)\/([A-z]+)\/\d+" ,
    #                                            r"\/players\/([a-z0-9]+)\/([A-z]+)\/([A-z]+)" ]
    #                                    )
    #     club_links = link_extractor.extract_links(response)
    #     for link in club_links :
    #         yield scrapy.Request(link.url, callback=self.parse_extract, headers={'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'})


    # def parse_extract(self, response): 
    #     links = response.xpath('//*[(@class="listhead" and contains(., "Match Logs (Summary)"))]/following-sibling::*[1]//a/@href')
    #     name = str(response.url).split("/")[-1]
    #     for link in list(set(links)):
    #         yield {
    #         "player_name": name,
    #         "match_logs_url": link
    #          }




#--------------------------SECTION 2-----------------------------------------------



    rules = (
        Rule(LinkExtractor(allow = r'\/players\/([a-z]+)',
                           restrict_xpaths=('//*[@class="section_wrapper"]')
                           ), 
            callback='parse_club_links', 
            follow=False),
        Rule(LinkExtractor(allow = r'\/players\/([a-z0-9]+)\/([A-z]+)',
                                       restrict_xpaths='//*[@class="section_wrapper"]',
                                       deny = [ r"\/players\/([a-z0-9]+)\/([A-z]+)\/\d+" ,
                                               r"\/players\/([a-z0-9]+)\/([A-z]+)\/([A-z]+)" ]
                                       ), 
            callback='parse_extract', follow=False),
    )



    credentials = botocore.credentials.Credentials(
        access_key='dummy',
        secret_key='dummy'
    )

    def parse_club_links(self, response):
        count = 0 
        link_extractor = LinkExtractor(allow = r'\/players\/([a-z0-9]+)\/([A-z]+)',
                                       restrict_xpaths='//*[@class="section_wrapper"]',
                                        deny = [ r"\/players\/([a-z0-9]+)\/([A-z]+)\/\d+" ,
                                               r"\/players\/([a-z0-9]+)\/([A-z]+)\/([A-z]+)" ]
                                       )
        club_links = link_extractor.extract_links(response)
        for link in club_links :
            yield scrapy.Request(link.url, callback=self.parse_extract, headers={'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'})


    def parse_extract(self, response): 
        links = response.xpath('//*[(@class="listhead" and contains(., "Match Logs (Summary)"))]/following-sibling::*[1]//a/@href').extract()
        name = str(response.url).split("/")[-1]
        for link in list(set(links)):
            yield {
            "player_name": name,
            "match_logs_url": link
             }




#--------------------------SECTION 3-----------------------------------------------

    # rules = (
    #     Rule(LinkExtractor(allow = r'\/players\/([a-z]+)',
    #                        restrict_xpaths=('//*[@class="section_wrapper"]')
    #                        ), 
    #         callback='parse_club_links', follow=False),
    # )
    
    # def parse_club_links(self, response):
    #     count = 0 
    #     link_extractor = LinkExtractor(allow = r'\/players\/([a-z0-9]+)\/([A-z]+)',
    #                                    restrict_xpaths='//*[@class="section_wrapper"]',
    #                                     deny = r"\/players\/([a-z0-9]+)\/([A-z]+)\/\d+"
    #                                    )
    #     club_links = link_extractor.extract_links(response)
    # #    print(response.url)
    #     attributes = {}
    #     count = 0 

    #     for link in club_links :
    #         #yield {"url": link.text, "text": link.url}
    #       #  print(link.url)
    #         print(link)
    #         return scrapy.Request(link.url, callback=self.parse_extract, headers={'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'})


    # def parse_extract(self, response):
    #     print("HERE",response.url)    
    #     links = response.xpath('//*[(@class="listhead" and contains(., "Match Logs (Summary)"))]/following-sibling::*[1]//a/@href')

    #     #links = LinkExtractor(restrict_xpaths='//*[(@class="listhead" and contains(text(), "Match Logs (Summary)"))]/following-sibling::*[1]')
    #   #  links = LinkExtractor()
    #   #  link_extractor_match_log = links.extract_links(response)    
    #     for link in links:
    #         yield scrapy.Request(response.urljoin(link), callback=self.parse_match_logs, headers={'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'})

    # def parse_match_logs(self, response):
    #     print("HERE",response.url)
    #     # extract desired data here and yield as item or dictionary
    #     yield {
    #         "player_name": response.xpath('//h1/text()').get(),
    #         "match_logs_url": response.url
    #     }