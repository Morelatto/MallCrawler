# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Compose, TakeFirst, Join

to_float = Compose(TakeFirst(), lambda v: v.replace('.', '').replace(',', '.'), float)
clean_text = Compose(MapCompose(lambda txt: txt.strip()), Join())


class Product(scrapy.Item):
    sku = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    price_discount = scrapy.Field()
    url = scrapy.Field()
    image = scrapy.Field()
    department = scrapy.Field()
    category = scrapy.Field()


class ProductLoader(ItemLoader):
    default_item_class = Product
    default_output_processor = TakeFirst()

    sku_out = Compose(TakeFirst(), lambda url: url.split('/')[4], int)
    name_out = clean_text
    price_out = to_float
    price_discount_out = to_float
    department_out = clean_text
    category_out = clean_text


class SondaDeliveryProduct(Product):
    sub_category = scrapy.Field()


class SondaDeliveryProductLoader(ProductLoader):
    default_item_class = SondaDeliveryProduct

    sub_category_out = clean_text
