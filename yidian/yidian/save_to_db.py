import pymongo
import logging

client = pymongo.MongoClient()
collections = client.pic.yidian
def save_to_db(item):
    result = collections.find_one(item)
    if not result:
        collections.insert_one(item)
        logging.warn(item['image_name']+"--开始保存")
        return True
    else:
        logging.warn(item['image_name']+"--已经存在")
        return False
