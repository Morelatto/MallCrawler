# -*- coding: utf-8 -*-
import scrapy

from smartcart.items import ProductLoader
from smartcart.items import ExtraDeliveryProduct


class ExtraDeliverySpider(scrapy.Spider):
    name = 'extra_delivery'
    allowed_domains = ['deliveryextra.com.br']
    start_urls = ['http://www.deliveryextra.com.br/']

    def parse(self, response):
        for department in response.xpath('//li[@class="nav-item nav-item-todos"]//a/@href').extract():
            yield scrapy.Request(department, callback=self.parse_categories)

    def parse_categories(self, response):
        for nav in response.xpath('//nav[@class="aside-nav"]'):
            if nav.xpath('.//h3[@class="aside-nav__heading"]/text()').extract_first().strip() == "Categoria:":
                for category in nav.xpath('.//a[@class="facetItemLabel aside-nav__link"]/@href').extract():
                    yield scrapy.Request(response.urljoin(category) + "&qt=36", callback=self.parse_products)
                break

    def parse_products(self, response):
        for product in response.xpath("//div[contains(concat(' ', normalize-space(@class), ' '), ' boxProduct ')]"):
            loader = ProductLoader(item=ExtraDeliveryProduct(), selector=product)

            loader.add_xpath('sku', './/a[@class="link"]/@href')
            loader.add_xpath('name', './/h3/a[@class="link"]/@title')
            loader.add_xpath('price', './/span[@class="value"]/text()')
            loader.add_xpath('price_discount', '(.//span[@class="value"]/text())[2]')
            loader.add_xpath('price_discount', 'concat('
                                               './/span[@class="yellow-side"]//span[@class="text-first-item"]/text(), '
                                               './/span[@class="yellow-side"]//span[@class="text-second-item"]/text())')
            loader.add_xpath('url', './/a[@class="link"]/@href')
            loader.add_xpath('image', './/img[@class="prdImagem img"]/@src')
            loader.add_xpath('department', '(//a[@class="breadcrumbs__label"]/@title)[2]')
            loader.add_xpath('category', '//span[@class="breadcrumbs__label breadcrumbs__label--current"]/text()')
            loader.add_xpath('status', 'boolean(.//span[@class="value"])')

            yield loader.load_item()

        next_page_url = response.xpath('//li[@class="pageSelect nextPage item inline--middle"]/a/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse_products)
