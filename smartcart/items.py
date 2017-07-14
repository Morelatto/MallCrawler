# -*- coding: utf-8 -*-
import scrapy

from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Compose, TakeFirst, Join
from w3lib.html import remove_tags as _remove_tags


to_float = Compose(TakeFirst(), lambda v: v.replace('.', '').replace(',', '.'), float)
to_int = Compose(TakeFirst(), int)
clean_text = Compose(MapCompose(lambda txt: txt.strip()), Join())
clean_sku = Compose(TakeFirst(), lambda url: url.split('/')[4], int)
remove_tags = Compose(MapCompose(_remove_tags), TakeFirst())


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

    sku_out = clean_sku
    name_out = clean_text
    price_out = to_float
    price_discount_out = to_float
    department_out = clean_text
    category_out = clean_text


class ExtraDeliveryProduct(Product):
    status = scrapy.Field()


class ExtraDeliveryProductLoader(ProductLoader):
    status_out = to_int


class SondaDeliveryProduct(Product):
    sub_category = scrapy.Field()


class SondaDeliveryProductLoader(ProductLoader):
    default_item_class = SondaDeliveryProduct

    sub_category_out = clean_text


class PaoDeAcucarProduct(Product):
    status = scrapy.Field()
    brand = scrapy.Field()
    description = scrapy.Field()


class PaoDeAcucarProductLoader(ProductLoader):
    default_item_class = PaoDeAcucarProduct

    sku_out = to_int
    price_out = TakeFirst()
    price_discount_out = TakeFirst()
    description_out = remove_tags
    brand_out = clean_text
    status_out = to_int
