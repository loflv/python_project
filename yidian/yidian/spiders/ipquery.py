# -*- coding: utf-8 -*-
import scrapy


class IpquerySpider(scrapy.Spider):
    name = 'ipquery'
    allowed_domains = []
    start_urls = ['http://httpbin.org/get']

    def parse(self, response):
        print(response.text)
