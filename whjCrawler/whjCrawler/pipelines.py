# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy.exceptions import DropItem

class WhjcrawlerPipeline(object):
    def __init__(self):
        self.file = open('result.jl', 'w', encoding='utf-8')
        # self.seen = set()  # 重复检测集合

    def process_item(self, item, spider):
        # if item['link'] in self.seen:
            # raise DropItem('Duplicate link %s' % item['link'])
        # self.seen.add(item['link'])
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()