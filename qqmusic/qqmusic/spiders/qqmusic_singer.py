# -*- coding: utf-8 -*-
import scrapy
import json
from urllib.parse import urlencode


class QqmusicSingerSpider(scrapy.Spider):
    name = 'qqmusic_singer'
    allowed_domains = ['qq.com']
    start_urls = ['http://qq.com/']


    def start_requests(self):
        #修改项目
        with open("C:/Users/Administrator/Desktop/python_exe/qq音乐.json", 'r') as f:
            songid = json.load(f)['qqmusic_singer']
            url = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_singer_track_cp.fcg?g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&ct=24&singermid=%s&order=listen&begin=0&num=10' % songid
            headers = {
                'referer': 'https://y.qq.com/n/yqq/singer/%s.html' % songid,
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
        songlist = json.loads(response.text)['data']['list']
        songsid = []  # 避免重复
        baseurl = 'https://u.y.qq.com/cgi-bin/musicu.fcg?'
        for song in songlist:
            songid = song['musicData']['songmid']
            songname = song['musicData']['songname']

            if not songsid.__contains__(songid):
                songsid.append(songid)
                str = '{"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"2031264230","songmid":["%s"],"uin":"0"}}}' % songid
                url = baseurl + urlencode({'data': str})
                yield scrapy.Request(url, callback=self.parse_music, meta={'name': songname})
