import scrapy
from itemloaders.processors import TakeFirst, MapCompose


def process_price(value):
    try:
        value = int(value.replace(' ', ''))
        return value
    except:
        return value


class LeroyItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(process_price))
    pictures = scrapy.Field()
    currency = scrapy.Field()
    unit = scrapy.Field()
    product_url = scrapy.Field()
    characteristicks = scrapy.Field()
