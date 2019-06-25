# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from fake_useragent import UserAgent


class AgentMiddleware(object):

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', UserAgent().random)
