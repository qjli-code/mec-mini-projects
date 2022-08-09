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
                'text': quote.xpath('./span[@class="text"]/text()').extract_first(),
                'author': quote.xpath('./span/small[@class="author"]/text()').extract_first(),
            }

        next_page = response.xpath(
            '//li[@class="next"]/a/@href').extract_first()
        #next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
