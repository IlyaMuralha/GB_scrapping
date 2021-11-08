import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from leroy.items import LeroyItem


class LeroyruSpider(scrapy.Spider):
    name = 'leroyru'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/mebel/']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath(
            '//div[@data-qa-pagination]//a[@data-qa-pagination-item="right"]/@href'
        ).extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath('//div[@data-qa-product]/a/@href')
        for link in links:
            yield response.follow(link, callback=self.product_parse)

    def product_parse(self, response: HtmlResponse):
        characteristicks = {}
        dl = response.xpath('//dl[@class="def-list"]/div')
        for i in dl:
            key = i.xpath('./dt/text()').extract_first()
            value = i.xpath('./dd/text()').extract_first()
            characteristicks[key] = value.replace('\n', '').strip()

        loader = ItemLoader(item=LeroyItem(), response=response)
        loader.add_xpath('name', '//h1//text()')
        loader.add_xpath('price', '//span[@slot="price"]/text()')
        loader.add_xpath('pictures', '//picture[@slot="pictures"]/img/@src')
        loader.add_xpath('currency', '//span[@slot="currency"]/text()')
        loader.add_xpath('unit', '//span[@slot="unit"]/text()')
        loader.add_value('product_url', response.url)
        loader.add_value('characteristicks', characteristicks)

        yield loader.load_item()
