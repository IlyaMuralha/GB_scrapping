import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://tyumen.hh.ru/search/vacancy?area=&fromSearchLine=true&'
                  'st=searchVacancy&text=Python&from=suggest_post']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@data-qa="pager-next"]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath(
            '//a[@data-qa="vacancy-serp__vacancy-title"]/@href'
        ).extract()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath('//h1[@data-qa="vacancy-title"]/text()').extract_first()
        min_salary = response.xpath('//p[@class="vacancy-salary"]/span/text()').extract_first()
        # vac_salary = response.css('p.vacancy-salary span::text').extract_first()
        # max_salary = min_salary
        # currency = min_salary
        url = response.url
        site_name = self.allowed_domains

        yield JobparserItem(name=name, min_salary=min_salary, url=url, site_name=site_name)
