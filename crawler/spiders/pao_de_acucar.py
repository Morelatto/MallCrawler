# -*- coding: utf-8 -*-
import scrapy
import json

from crawler.items import PaoDeAcucarProductLoader
from urllib import urlencode
from urlparse import parse_qs, urlsplit, urlunsplit


def set_query_parameters(url, params):
    scheme, netloc, path, query_string, fragment = urlsplit(url)
    query_params = parse_qs(query_string.encode('utf-8'))

    for param_name, param_value in params.iteritems():
        query_params[param_name] = str(param_value).encode('utf-8')

    new_query_string = urlencode(query_params, doseq=True)
    return urlunsplit((scheme, netloc, path, new_query_string, fragment))


class PaoDeAcucarSpider(scrapy.Spider):
    name = 'pao_de_acucar'
    allowed_domains = ['paodeacucar.com', 'api.gpa.digital']
    start_urls = ['https://api.gpa.digital/pa/detail/categories?storeId=501&split=&showSub=true']

    def parse(self, response):
        json_response = json.loads(response.body_as_unicode())
        if json_response.get('status', '') == 'success':
            for department in json_response.get('content'):
                yield scrapy.Request(
                    set_query_parameters(response.urljoin('/pa/products/list' + department.get('link')),
                                         {'storeId': 501}),
                    meta=dict(department=department.get('name')),
                    callback=self.parse_categories
                )

    def parse_categories(self, response):
        json_response = json.loads(response.body_as_unicode())
        if json_response.get('status', '') == 'success':
            for category in json_response.get('content').get('sideBarMenu').get('navList')[0].get('navItemList'):
                yield scrapy.Request(
                    set_query_parameters(response.urljoin('/pa/products/list' + category.get('url')),
                                         {'storeId': 501, 'qt': 36}),
                    meta=dict(department=response.meta.get('department'), category=category.get('title')),
                    callback=self.parse_products)

    def parse_products(self, response):
        json_response = json.loads(response.body_as_unicode())
        if json_response.get('status', '') == 'success':
            for product in json_response.get('content').get('products'):
                loader = PaoDeAcucarProductLoader(selector=product)

                loader.add_value('sku', product.get('sku'))
                loader.add_value('name', product.get('name'))
                loader.add_value('price', product.get('priceFrom'))
                loader.add_value('price', product.get('currentPrice'))
                loader.add_value('price_discount', product.get('currentPrice') if product.get('priceFrom') else '')
                loader.add_value('url', 'https://www.paodeacucar.com')
                loader.add_value('url', product.get('urlDetails'))
                loader.add_value('image', 'https://www.paodeacucar.com')
                loader.add_value('image', product.get('mapOfImages').get('0').get('BIG'))
                loader.add_value('description', product.get('shortDescription'))
                loader.add_value('category', response.meta.get('category'))
                loader.add_value('status', product.get('stock'))
                loader.add_value('brand', product.get('brand'))
                loader.add_value('department', response.meta.get('department'))

                yield loader.load_item()

            if json_response.get('content').get('number') < json_response.get('content').get('totalPages') - 1:
                yield scrapy.Request(
                    set_query_parameters(response.url, {'p': json_response.get('content').get('number') + 1}),
                    meta=dict(department=response.meta.get('department'), category=response.meta.get('category')),
                    callback=self.parse_products
                )
