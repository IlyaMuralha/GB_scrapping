import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SgruSpider(scrapy.Spider):
    name = 'sgru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python&noGeo=1']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath(
            '//a[contains(@class, "f-test-button-dalshe")]/@href'
        ).extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath(
            '//div[contains(@class, "f-test-vacancy-item")]//a[contains(@target, "_blank")]/@href').extract()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath(
            '//div[contains(@class, "vacancy-base-info")]//h1/text()'
        ).extract_first()
        min_salary = ''.join(response.xpath(
            '//div[contains(@class, "vacancy-base-info")]//h1/following-sibling::span/descendant::text()').getall()
                             )
        url = response.url
        site_name = self.allowed_domains

        yield JobparserItem(name=name, min_salary=min_salary, url=url, site_name=site_name)
