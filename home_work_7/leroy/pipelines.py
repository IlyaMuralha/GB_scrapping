import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class LeroyPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client['Leroy_Merlin']

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.update_one(item)
        return item


class LeroyPhotosPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item['pictures']:
            for img in item['pictures']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['pictures'] = [itm[1] for itm in results if itm[0]]
        return item
