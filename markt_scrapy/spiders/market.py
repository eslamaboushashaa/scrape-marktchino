import scrapy
from ..items import MarktScrapyItem


class MarketSpider(scrapy.Spider):
    name = 'market'

    start_urls = ['https://www.marketchino.com/ar/handmade.html?___from_store=en&limit=all']

    def parse(self, response):

        links = response.css('.product-name>a::attr(href)').extract()
        try:
            for link in links:
                yield scrapy.Request(response.urljoin(link), callback=self.parse_page)
        except:
            print("no request")

    def parse_page(self, response):
        items =MarktScrapyItem()
        name = response.css('div.product-name>h1::text').extract()
        review = response.css('p.rating-links>a::text').extract()
        price = response.css('div.product-info>div>div.price-box>span.regular-price>span.price::text').extract()
        number_availability = response.css('p.availability-only>span::attr(title)').extract()
        sold_by = response.css('span.wk_block_title_css>a::text').extract()
        descriptive = response.css('div#tab_additional_tabbed_contents>table.data-table>tbody>tr>td::text')[3].extract()

        items['name'] = name
        items['review'] = review
        items['price'] = price
        items['number_availability'] = number_availability
        items['sold_by'] = sold_by
        items['description'] = descriptive
        yield items

