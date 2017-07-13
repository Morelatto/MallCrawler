# -*- coding: utf-8 -*-

from datetime import datetime
from hashlib import md5
from twisted.enterprise import adbapi

from smartcart.items import SondaDeliveryProduct, PaoDeAcucarProduct, ExtraDeliveryProduct


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
        if type(item) is ExtraDeliveryProduct:
            return self._handle_extra(conn, item, spider)
        if type(item) is SondaDeliveryProduct:
            return self._handle_sonda(conn, item, spider)
        if type(item) is PaoDeAcucarProduct:
            return self._handle_pao_de_acucar(conn, item, spider)

    def _handle_extra(self, conn, item, spider):
        guid = self._get_guid(item)
        now = datetime.utcnow().replace(microsecond=0).isoformat(' ')

        item_data = (
            item.get('sku', ''),
            item.get('name', '').replace("'", "''"),
            item.get('price', None),
            item.get('price_discount', None),
            item.get('url', ''),
            item.get('image', ''),
            item.get('department', ''),
            item.get('category', ''),
            item.get('status'),
        )

        conn.execute("SELECT EXISTS(SELECT 1 FROM EXTRA_DELIVERY_PRODUCTS WHERE guid = %s)", (guid,))

        if conn.fetchone()[0]:
            conn.execute(
                "UPDATE EXTRA_DELIVERY_PRODUCTS SET sku=%s, `name`=%s, price=%s, price_discount=%s, url=%s, image=%s, "
                "department=%s, category=%s, `status`=%s WHERE guid=%s", item_data + (guid,)
            )
            spider.logger.debug("Item updated in db: {} {}".format(guid, item))
        else:
            conn.execute(
                "INSERT INTO EXTRA_DELIVERY_PRODUCTS (guid, sku, `name`, price, price_discount, url, image, department,"
                " category, `status`, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (guid,) + item_data + (now,)
            )
            spider.logger.debug("Item stored in db: {} {}".format(guid, item))

    def _handle_sonda(self, conn, item, spider):
        pass

    def _handle_pao_de_acucar(self, conn, item, spider):
        pass

    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        # do nothing, just log
        spider.logger.error(failure)

    def _get_guid(self, item):
        """Generates an unique identifier for a given item."""
        # hash based solely in the url field
        return md5(item.get('url').encode()).hexdigest()
