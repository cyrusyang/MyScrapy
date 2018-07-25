# -*- coding: utf-8 -*-
import scrapy


class DemoSpider(scrapy.Spider):
    name = "demo"
    allowed_domains = ["zimuku.net"]
    start_urls = ['http://zimuku.net/']

    def parse(self, response):
        name = response.xpath('//b/text()').extract()[1]

        # 建立一个items字典，用于保存我们爬到的结果，并返回给pipline处理
        items = {}
        items['第一个'] = name

        return items
