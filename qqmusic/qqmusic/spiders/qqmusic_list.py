# -*- coding: utf-8 -*-
import scrapy
import json
from fake_useragent import UserAgent
from urllib.parse import urlencode


class QqmusicSingerSpider(scrapy.Spider):
    name = 'qqmusic_list'
    allowed_domains = ['qq.com']
    start_urls = ['http://qq.com/']


    def start_requests(self):
        url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?data=%7b%22detail%22%3a%7b%22module%22%3a%22musicToplist.ToplistInfoServer%22%2c%22method%22%3a%22GetDetail%22%2c%22param%22%3a%7b%22topId%22%3a4%2c%22offset%22%3a0%2c%22num%22%3a30%7d%7d%7d'
        headers = {
            'referer': 'https://y.qq.com/',
            'User-agent': UserAgent().random
        }
        yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse_td(self, response):
        yield {
            'name': response.meta['name'],
            'content': response.body
        }

    def parse_music(self, response):
        url_end = json.loads(response.text)['req_0']['data']['midurlinfo'][0]['purl']
        url = "http://isure.stream.qqmusic.qq.com/" + url_end
        yield scrapy.Request(url, meta={'name': response.meta['name']}, callback=self.parse_td)

    def parse(self, response):
        songlist = json.loads(response.text)['detail']['data']['songInfoList']
        songsid = []  # 避免重复
        baseurl = 'https://u.y.qq.com/cgi-bin/musicu.fcg?'

        headers = {
            'referer': 'https://y.qq.com/',
            'User-agent': UserAgent().random
        }
        for song in songlist:
            songid = song['mid']
            songname = song['name']

            if not songsid.__contains__(songid):
                songsid.append(songid)
                str = '{"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch","param":{"guid":"2031264230","calltype":0,"userip":""}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"2031264230","songmid":["%s"],"uin":"41946468","loginflag":1,"platform":"20"}}}' % songid
                url = baseurl + urlencode({'data': str})
                yield scrapy.Request(url, callback=self.parse_music, headers=headers,meta={'name': songname})
