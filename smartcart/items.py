# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Compose, TakeFirst, Join

to_float = Compose(TakeFirst(), lambda v: v.replace('.', '').replace(',', '.'), float)


class ExtraDeliveryProduct(scrapy.Item):
    sku = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    price_discount = scrapy.Field()
    url = scrapy.Field()
    image = scrapy.Field()
    department = scrapy.Field()
    category = scrapy.Field()


class ExtraDeliveryProductLoader(ItemLoader):
    default_item_class = ExtraDeliveryProduct
    default_output_processor = TakeFirst()

    sku_out = Compose(TakeFirst(), lambda url: url.split('/')[4], int)
    name_out = Compose(MapCompose(lambda txt: txt.strip()), Join())
    price_out = to_float
    price_discount_out = to_float
