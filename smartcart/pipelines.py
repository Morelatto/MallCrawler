# -*- coding: utf-8 -*-

from hashlib import md5
from scrapy.exceptions import DropItem
from smartcart.items import SondaDeliveryProduct, PaoDeAcucarProduct, ExtraDeliveryProduct
from twisted.enterprise import adbapi


class ExtraDeliveryMySQLPipeline(object):
    """A pipeline to store the item in a MySQL database.
    This implementation uses Twisted's asynchronous database API.
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        # run db query in the thread pool
        d = self.dbpool.runInteraction(self._do_upsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        # at the end return the item in case of success or failure
        d.addBoth(lambda _: item)
        # return the deferred instead the item. This makes the engine to
        # process next item (according to CONCURRENT_ITEMS setting) after this
        # operation (deferred) has finished.
        return d

    def _do_upsert(self, conn, item, spider):
        """Perform an insert or update."""
        guid = self._get_guid(item)

        item_data = (
            item.get('sku'),
            item.get('name'),
            item.get('price'),
            item.get('price_discount'),
            item.get('url'),
            item.get('image'),
            item.get('department'),
            item.get('category'),
        )

        update_fields = 'sku=%s, `name`=%s, price=%s, price_discount=%s, url=%s, image=%s, department=%s, category=%s, '
        insert_fields = 'sku, `name`, price, price_discount, url, image, department, category, '

        if type(item) is ExtraDeliveryProduct:
            table_name = 'EXTRA_DELIVERY_PRODUCTS'
            item_data += (item.get('status'),)
            update_fields += '`status`=%s'
            insert_fields += '`status`'

        elif type(item) is SondaDeliveryProduct:
            table_name = 'SONDA_DELIVERY_PRODUCTS'
            item_data += (item.get('sub_category'),)
            update_fields += 'sub_category=%s'
            insert_fields += 'sub_category'

        elif type(item) is PaoDeAcucarProduct:
            table_name = 'PAO_DE_ACUCAR_PRODUCTS'
            item_data += (item.get('status'), item.get('brand'), item.get('description'),)
            update_fields += '`status`=%s, brand=%s, description=%s'
            insert_fields += '`status`, brand, description'
        else:
            raise DropItem('Invalid item class {}: {}'.format(type(item), item))

        conn.execute("SELECT EXISTS(SELECT 1 FROM {} WHERE guid = %s)".format(table_name), (guid, ))

        if conn.fetchone()[0]:
            conn.execute("UPDATE {} SET {} WHERE guid=%s".format(table_name, update_fields), item_data + (guid,))
            spider.logger.debug("Item updated in db: {} {}".format(guid, item))
        else:
            conn.execute("INSERT INTO {} (guid, {}) VALUES ({} %s)".format(table_name, insert_fields,
                                                                        (insert_fields.count(',') + 1) * '%s, '),
                         (guid,) + item_data)
            spider.logger.debug("Item stored in db: {} {}".format(guid, item))

    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        # do nothing, just log
        spider.logger.error("Item failed {}".format(item))
        spider.logger.error(failure)

    def _get_guid(self, item):
        """Generates an unique identifier for a given item."""
        # hash based solely in the url field
        return md5(item.get('url').encode()).hexdigest()
