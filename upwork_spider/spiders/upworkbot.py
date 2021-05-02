import scrapy
from ..items import UpworkSpiderItem

class UpworkSpiderBot(scrapy.Spider):
    
    name = 'upworkscraper'
    page_number = 2

    start_urls = ["http://www.upwork.com/search/jobs/?from_recent_search=true&q=power%20bi&sort=recency"]

    def parse(self, response):

        ## Import the item class for data storage from items.py
        item = UpworkSpiderItem()

        # print(response.text)
        descriptions = response.css(".d-xl-block::text").extract()
        prices = response.css(".text-muted .text-muted::text").extract()

        for (description, price) in zip(descriptions, prices):        
            # Storing the extracted data into the items class we created
            item['descriptions'] = description.strip()
            item['prices'] = price.strip()

            # yield {'Title': title.encode('utf-8'), 'Vote': vote, "Comments": comment}
            yield item
        

        next_page = "https://www.upwork.com/search/jobs/?page=" + str(UpworkSpiderBot.page_number) + "&q=power%20bi&sort=recency"
        UpworkSpiderBot.page_number+=1
        if UpworkSpiderBot.page_number<30:
            yield response.follow(next_page, callback = self.parse)

