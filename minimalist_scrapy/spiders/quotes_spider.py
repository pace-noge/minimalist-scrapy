import scrapy


class QuotesSpiderSpider(scrapy.Spider):
    name = 'quotes_spider'
    # allowed_domains = ['http://quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/page/1/']

    def parse(self, response):
        self.logger.info('Quotes Spider')
        quotes = response.css('div.quote')
        for quote in quotes:
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall()
            }
            author_url = quote.css('.author + a::attr(href)').get()
            self.logger.info("Processing Author")
            yield response.follow(author_url, callback=self.parse_author)
        # next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
        #    yield response.follow(next_page, callback=self.parse)
        yield from response.follow_all(css='ul.pager a', callback=self.parse)


    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
            'born_location': extract_with_css(
                '.author-born-location::text'
            ),
            'bio': extract_with_css('.author-description::text')

        }
