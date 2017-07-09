# -*- coding: utf-8 -*-
import scrapy

from smartcart.items import SondaDeliveryProductLoader


class ExtraDeliverySpider(scrapy.Spider):
    name = 'sonda_delivery'
    allowed_domains = ['sondadelivery.com.br']
    start_urls = ['http://www.sondadelivery.com.br/']

    def parse(self, response):
        for department in response.xpath(
                '//a[boolean(number(substring-before(substring-after(@id, "ctl00_menuPrincipal_ctl"), "_linkMenu")))]'):
            yield scrapy.Request(response.urljoin(department.xpath('.//@href').extract_first()),
                                 meta=dict(department=department.xpath('.//text()').extract_first()),
                                 callback=self.parse_categories)

    def parse_categories(self, response):
        for category in response.xpath('//div[@class="col-sm-8 col-md-6"]//li'):
            sub_categories = category.xpath('.//a')
            quantity = len(sub_categories.extract())
            if quantity > 1:
                category_name = None
                for index, name, url in zip(range(quantity), sub_categories.xpath('.//text()').extract(),
                                            sub_categories.xpath('.//@href').extract()):
                    if not index:
                        category_name = name
                    else:
                        yield scrapy.Request(response.urljoin(url),
                                             meta=dict(department=response.meta.get("department"),
                                                       category=category_name, sub_category=name),
                                             callback=self.parse_products)

    def parse_products(self, response):
        for product in response.xpath('//div[@class="row product-list"]//div[@class="product"]'):
            loader = SondaDeliveryProductLoader(selector=product)

            loader.add_xpath('sku', './/a[@itemprop="url"]/@href')
            loader.add_xpath('name', './/span[@class="tit"]/text()')
            loader.add_xpath('url', './/a[@itemprop="url"]/@href')
            loader.add_xpath('price', './/span[@class="price"]//span[not (@class)]/text()')
            loader.add_xpath('price_discount', './/span[@class="valor-por-sonda"]//span/text()')
            loader.add_xpath('image', './/img/@src')
            loader.add_value('department', response.meta.get("department"))
            loader.add_value('category', response.meta.get("category"))
            loader.add_value('sub_category', response.meta.get("sub_category"))

            yield loader.load_item()

        next_page_url = response.xpath('//a[@id="ctl00_conteudo_linkPaginaProxima"]/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url),
                                 meta=dict(department=response.meta.get("department"),
                                           category=response.meta.get("category"),
                                           sub_category=response.meta.get("sub_category")),
                                 callback=self.parse_products)
