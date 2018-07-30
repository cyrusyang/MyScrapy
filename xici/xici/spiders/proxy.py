# -*- coding: utf-8 -*-
import scrapy

from xici.items import XiciItem


class ProxySpider(scrapy.Spider):
    name = "proxy"
    allowed_domains = ["www.xicidaili.com"]
    start_urls = ['http://www.xicidaili.com/nn/1']

    def parse(self, response):
        """
                爬取xici代理
                :param response:
                :return:
                """
        trs = response.xpath('//table[@id="ip_list"]/tr[@class]')
        for tr in trs:
            item = XiciItem()
            item['ip'] = tr.xpath('td[2]/text()').extract()[0]
            item['port'] = tr.xpath('td[3]/text()').extract()[0]
            item['protocol'] = str(tr.xpath('td[6]/text()').extract()[0]).lower()
            yield item
