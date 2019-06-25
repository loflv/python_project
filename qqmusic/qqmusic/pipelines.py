# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from qqmusic.save_to_db import save_to_db


class QqmusicPipeline(object):
    def process_item(self, item, spider):
        content = item['content']
        name = item['name']

        result = save_to_db({'song_name':item['name']})
        if result:
            with open("f://qq音乐/" + name+".mp3", 'wb+') as f:
                f.write(content)
