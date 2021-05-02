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
        urls = response.css(".visited::attr(href)").extract()
        

        print("Currently on page number: " + str(UpworkSpiderBot.page_number))
        for (description, price, url) in zip(descriptions, prices, urls):        
            # Storing the extracted data into the items class we created
            item['descriptions'] = ' '.join(description.split())
            item['prices'] = price.strip()
            item['links'] = url

            yield item
        

        next_page = "https://www.upwork.com/search/jobs/?page=" + str(UpworkSpiderBot.page_number) + "&q=power%20bi&sort=recency"
        UpworkSpiderBot.page_number+=1
        if UpworkSpiderBot.page_number<30:
            yield response.follow(next_page, callback = self.parse)

