# -*- coding: utf-8 -*-
import scrapy


class ExtraDeliverySpider(scrapy.Spider):
    name = 'sonda_delivery'
    allowed_domains = ['sondadelivery.com.br']
    start_urls = ['http://www.sondadelivery.com.br/']

    def parse(self, response):
        for department in response.xpath('//a[boolean(number(substring-before(substring-after(@id, "ctl00_menuPrincipal_ctl"), "_linkMenu")))]/@href').extract():
            yield scrapy.Request(response.urljoin(department), meta=dict(department=""),callback=self.parse_categories)

    def parse_categories(self, response):
        pass
