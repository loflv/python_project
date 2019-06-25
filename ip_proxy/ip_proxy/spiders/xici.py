# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
from scrapy.http import HtmlResponse


class XiciSpider(scrapy.Spider):
    name = 'xici'
    allowed_domains = []
    start_urls = ['https://www.xicidaili.com/nn']

    def call_fu(self, response):
        print(response)

    def parse(self, response):
        trs = response.xpath("//table[@id=\"ip_list\"]//tr")
        for tr in trs:
            mes = tr.xpath("string(.)").extract()[0].strip().split("\n")
            if mes[1].strip().isnumeric():
                url = "%s:%s" % (mes[0].strip(), mes[1].strip())
                proxy1 = "http://%s" % url
                proxy2 = "https://%s" % url
                yield scrapy.Request("http://httpbin.org/get", meta={'proxy': proxy1},  callback=self.call_fu)
