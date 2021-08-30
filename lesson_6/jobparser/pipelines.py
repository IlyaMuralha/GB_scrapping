# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client['vacancies2408']

    def process_item(self, item, spider):
        print()
        if spider.name == 'hhru':
            try:
                salary = item['min_salary'].split(' ')
                if len(salary) == 5:
                    min_salary = int(''.join(salary[1].split('\xa0')))
                    max_salary = int(''.join(salary[3].split('\xa0')))
                    currency = salary[-1]
                if len(salary) == 3:
                    if salary[0] == 'до':
                        min_salary = None
                        max_salary = int(''.join(salary[1].split('\xa0')))
                        currency = salary[-1]
                    elif salary[0] == 'от':
                        min_salary = int(''.join(salary[1].split('\xa0')))
                        max_salary = None
                        currency = salary[-1]
                elif salary[0] == 'з/п':
                    min_salary, max_salary, currency = None, None, None
            except Exception as err:
                print(f'{type(err)}:\n{err}')

        elif spider.name == 'sgru':
            try:
                salary = item['min_salary'].replace('\xa0', ' ').split(' ')
                print(salary)
                if len(salary) == 6:
                    min_salary = int(''.join(salary[0]) + ''.join(salary[1]))
                    max_salary = int(''.join(salary[3]) + ''.join(salary[4]))
                    currency = salary[-1]
                elif len(salary) == 4:
                    if salary[0] == 'до':
                        min_salary = None
                        max_salary = int(''.join(salary[1]) + ''.join(salary[2]))
                        currency = salary[-1]
                    elif salary[0] == 'от':
                        min_salary = int(''.join(salary[1]) + ''.join(salary[2]))
                        max_salary = None
                        currency = salary[-1]
                elif len(salary) == 3:
                    min_salary = int(''.join(salary[0]) + ''.join(salary[1]))
                    max_salary = None
                    currency = salary[-1]
                elif salary[0] == 'По':
                    min_salary, max_salary, currency = None, None, None
            except Exception as err:
                print(f'{type(err)}:\n{err}')

        item['min_salary'] = min_salary
        item['max_salary'] = max_salary
        item['currency'] = currency
        item['site_name'] = str(item['site_name']).replace("[", "").replace("]", "").replace("'", "")

        collection = self.mongo_base[spider.name]
        collection.update_one(
            {'url': item['url']},
            {'$set': item},
            upsert=True
        )
        # collection.insert_one(item)

        return item
