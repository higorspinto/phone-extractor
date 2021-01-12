# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class PhoneExtractorPipeline:
    website_list = []

    def process_item(self, item, spider):
        self.website_list.append(json.dumps(item))
        return item

    def close_spider(self, spider):
        for website in self.website_list:
            print(website)