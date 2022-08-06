from gc import callbacks
import scrapy


class CSSQuoteSpider(scrapy.Spider):
    name = 'toscrape-xpath'

    def start_requests(self):
        url = 'http://quotes.toscrape.com/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'text': quote.xpath('./span/text()').get(),
                'author': quote.xpath('./span/small/text()').get(),
            }

        #next_page = response.xpath('//li/a/@href').get()
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
