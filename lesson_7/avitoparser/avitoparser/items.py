import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def process_split_price(value):
    value1 = value.split('\xa0')
    value = int(value1[0] + value1[1])
    return value


class AvitoparserItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    price = scrapy.Field(input_processor=MapCompose(process_split_price),
                         output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    site_name = scrapy.Field(output_processor=TakeFirst())
    _id = scrapy.Field()
