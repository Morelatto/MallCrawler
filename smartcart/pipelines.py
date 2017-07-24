# -*- coding: utf-8 -*-

from hashlib import md5
from scrapy.exceptions import DropItem
from smartcart.items import SondaDeliveryProduct, PaoDeAcucarProduct, ExtraDeliveryProduct
from twisted.enterprise import adbapi


def extract_field_names(item, extra=''):
    return ''.join(['`{}`{}, '.format(key, extra) for key in item.keys()])[:-2]


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

        if type(item) is ExtraDeliveryProduct:
            table_name = 'EXTRA_DELIVERY_PRODUCTS'
        elif type(item) is SondaDeliveryProduct:
            table_name = 'SONDA_DELIVERY_PRODUCTS'
        elif type(item) is PaoDeAcucarProduct:
            table_name = 'PAO_DE_ACUCAR_PRODUCTS'
        else:
            raise DropItem('Invalid item class {}: {}'.format(type(item), item))

        conn.execute("SELECT EXISTS(SELECT 1 FROM {} WHERE guid = %s)".format(table_name), (guid,))

        if conn.fetchone()[0]:
            update_stmt = "UPDATE {} SET {} WHERE `guid`=%s".format(table_name, extract_field_names(item, '=%s'))
            conn.execute(update_stmt, tuple(item.values()) + (guid,))
            spider.logger.debug("Item updated in db: {} {}".format(guid, item))
        else:
            insert_stmt = "INSERT INTO {} (`guid`, {}) VALUES ({}%s)".format(table_name, extract_field_names(item),
                                                                             '%s, ' * len(item))
            conn.execute(insert_stmt, (guid,) + tuple(item.values()))
            spider.logger.debug("Item inserted in db: {} {}".format(guid, item))

    # noinspection PyMethodMayBeStatic
    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        # do nothing, just log
        spider.logger.error("Item failed {}".format(item))
        spider.logger.error(failure)

    # noinspection PyMethodMayBeStatic
    def _get_guid(self, item):
        """Generates an unique identifier for a given item."""
        # hash based solely in the url field
        return md5(item.get('url').encode()).hexdigest()
