from itemadapter import ItemAdapter
import csv


class InstaparserPipeline:
    def process_item(self, item, spider):
        return item


class CSVPipeline(object):
    def __init__(self):
        self.file = 'database.csv'
        with open(self.file, 'r', newline='') as csv_file:
            self.tmp_data = csv.DictReader(csv_file).fieldnames

        self.csv_file = open(self.file, 'a', newline='', encoding='utf-8')

    def process_item(self, item, spider):
        colums = item.fields.keys()

        data = csv.DictWriter(self.csv_file, colums)
        if not self.tmp_data:
            data.writeheader()
            self.tmp_data = True
        data.writerow(item)
        return item

    def __del__(self):
        self.csv_file.close()
