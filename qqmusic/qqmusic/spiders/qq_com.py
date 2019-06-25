# -*- coding: utf-8 -*-
import scrapy
import json
from fake_useragent import UserAgent
from urllib.parse import urlencode


class QqComSpider(scrapy.Spider):
    name = 'qqmusic'
    allowed_domains = ['qq.com']
    start_urls = ['https://y.qq.com/n/yqq/playsquare/2339470106.html#stat=y_new.index.playlist.pic']

    def start_requests(self):
        #修改项目
        ubun_id = 2356114935
        url = 'https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg?type=1&disstid=%d&format=json' % ubun_id
        headers = {
            'referer': 'https://y.qq.com/n/yqq/playsquare/%d.html' % ubun_id,
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
        songlist = json.loads(response.text).get('cdlist')[0]['songlist']
        songsid = []  # 避免重复
        baseurl = 'https://u.y.qq.com/cgi-bin/musicu.fcg?'
        for song in songlist:
            songid = song['songmid']
            songname = song['songname']

            if not songsid.__contains__(songid):
                songsid.append(songid)
                str = '{"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"2031264230","songmid":["%s"],"songtype":[0],"uin":"0"}}}' % songid
                url = baseurl + urlencode({'data': str})
                yield scrapy.Request(url, callback=self.parse_music, meta={'name': songname})
