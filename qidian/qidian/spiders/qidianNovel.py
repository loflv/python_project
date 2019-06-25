# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class QidiannovelSpider(CrawlSpider):
    name = 'qidianNovel'
    allowed_domains = ['bqg3.com']
    start_urls = ['https://www.bqg3.com/12_12720/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//*[@id="list"]/dl/dd[1]/a'), callback='parse_item',
             follow=True),
        Rule(LinkExtractor(restrict_xpaths="//*[@id='wrapper']/div[1]/div/div[2]/div/a[4]"),
             callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        title = response.xpath('//*[@id="wrapper"]/div[1]/div/div[2]/h1/text()').extract_first()
        content = ''.join(response.xpath('//*[@id="content"]/text()').extract())
        next_url = response.xpath("//*[@id='wrapper']/div[1]/div/div[2]/div/a[4]/text()").extract()
        yield {'title': title, 'content': content}
