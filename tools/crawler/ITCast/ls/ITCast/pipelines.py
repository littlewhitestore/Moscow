# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import sys


class ItcastPipeline(object):

    def open_spider(self, spider):
        self.file_name = open("itcast.json", "w")
        # self.file_name = self.file_name.readlines()
        # reload(sys)
        # sys.setdefaultencoding("utf-8")
        # self.file_name = self.file_name.decode("utf-8")
        # return self.file_name

    def process_item(self, item, spider):
        content = json.dumps(dict(item)) + ",\n"
        self.file_name.write(content)
        return item



    def close_spider(self, spider):
        self.file_name.close()
