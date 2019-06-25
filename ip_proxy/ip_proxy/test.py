import json
import threading

from lxml import etree
from requests import get
from fake_useragent import UserAgent
import pymongo

client = pymongo.MongoClient()
collections = client.proxy.xici

headers = {
    "User-Agent": UserAgent().random
}


def get_proxy():
    proxy_url = tr.xpath("string(.)").strip().split("\n")
    if proxy_url[1].strip().isnumeric():
        url = "%s:%s" % (proxy_url[0].strip(), proxy_url[1].strip())
        proxy1 = {"http": "http://%s" % url, "https": "https://%s" % url}
        try:
            res = get("http://httpbin.org/get", headers=headers, proxies=proxy1, timeout=8)
            if res.status_code == 200:
                js = json.loads(res.text)
                if js['origin'].split(',')[0] == proxy_url[0].strip():
                    if not (collections.find_one({"url": url})):
                        collections.insert_one({"url": url})
        except Exception as e:  # 捕捉异常
            print('请求失败,出现的错误是%s ' % e)


class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        get_proxy()


xici_reps = get("https://www.xicidaili.com/nn", headers=headers)
etree = etree.HTML(xici_reps.text)
trs = etree.xpath("//table[@id=\"ip_list\"]//tr")

for tr in trs:
    thread = myThread()
    thread.start()
