# -*- coding: utf-8 -*-
import json
import logging

import scrapy
from scrapy.spiders import CrawlSpider


# 将数字替换成对赢的字符

def del_url_name(del_num):
    trade = {
        "1": "%3B",
        "2": "8",
        "3": "9",
        "4": "%3E",
        "5": "%3F",
        "6": "%3C",
        "7": "%3D",
        "8": "2",
        "9": "3",
        "0": "%3a"
    }

    if del_num >= 1000:
        i1 = del_num // 1000
        i2 = (del_num - i1 * 1000) // 100
        i3 = (del_num - i1 * 1000 - i2 * 100) // 10
        i4 = del_num - i1 * 1000 - i2 * 100 - i3 * 10
        return trade[str(i1)] + trade[str(i2)] + trade[str(i3)] + trade[str(i4)]
    elif del_num >= 100:
        i1 = del_num // 100
        i2 = (del_num - i1 * 100) // 10
        i3 = del_num - i1 * 100 - i2 * 10
        return trade[str(i1)] + trade[str(i2)] + trade[str(i3)]
    elif del_num >= 10:
        i1 = del_num // 10
        i2 = del_num - i1 * 10
        return trade[str(i1)] + trade[str(i2)]
    else:
        return trade[str(del_num)]


# 得到下一次的url地址
def dealurl(start):
    end = start + 10
    if start > 9999 or end > 9999:
        pass
    url_base = "http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=12535072592&cstart=" + str(
        start) + "&cend=" + str(end) + "&_spt=yz~eaod%3B8%3F9%3F%3A%3D8%3F38"
    return url_base + del_url_name(start) + del_url_name(end)


class YidianSpider(CrawlSpider):
    name = 'yidian'
    allowed_domains = ['yidianzixun.com']
    start_urls = []

    def start_requests(self):
        url = 'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=12535072592&cstart=10&cend=20&_spt=yz~eaod%3B8%3F9%3F%3A%3D8%3F38%3B%3A8%3A'
        heanders = {
            'Referer': 'http://www.yidianzixun.com/channel/u241'
        }
        yield scrapy.Request(url, headers=heanders, u={'start': 10})

    def parse(self, response):
        start = response.meta['start']
        content = json.loads(response.text)
        imagurls = []
        if content and "result" in content:
            tict_result = content.get('result')
            for tict in tict_result:
                imgurl = tict['image']
                imagurls.append(imgurl)
            yield {
                'image_urls': imagurls
            }
        else:
            logging.warn(response.url + "---获取失败")

        heanders = {
            'Referer': 'http://www.yidianzixun.com/channel/u241',
            'cookie': 'JSESSIONID=7cc0f134c3ba92bcef9a596011bc6b2b7276832ce61d16524c0dd20b2c195d14; wuid=439287758011843; wuid_createAt=2019-04-09 20:27:07; UM_distinctid=16a0210fbe16ee-0fab22d6d6111f-7a1b34-144000-16a0210fbe26fd; radius=220.152.220.88; CNZZDATA1276509685=2042583036-1554999321-https%253A%252F%252Fwww.baidu.com%252F%7C1554999321; weather_auth=2; Hm_lvt_15fafbae2b9b11d280c79eff3b840e45=1554994135,1554999329,1555078579,1555083274; CNZZDATA1255169715=1929822595-1554810888-null%7C1555087750; captcha=s%3A4d5079e76b23742a8bcf2bee0f7b71fd.70hnuGbBlKyT8nwyKw22hDckt7g192fDkft0awgpQj8; Hm_lpvt_15fafbae2b9b11d280c79eff3b840e45=1555090191; cn_1255169715_dplus=%7B%22distinct_id%22%3A%20%2216a0210fbe16ee-0fab22d6d6111f-7a1b34-144000-16a0210fbe26fd%22%2C%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201555090186%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201555090186%7D'
        }
        url = dealurl(start)
        start += 10
        if start < 9999:
            yield scrapy.Request(url, meta={'start': start}, headers=heanders, dont_filter=True, callback=self.parse)
