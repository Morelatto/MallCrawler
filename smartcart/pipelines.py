# -*- coding: utf-8 -*-

from hashlib import md5
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
            guid, item.get('sku', ''), item.get('name', '').replace("'", "''"), item.get('price', 0),
            item.get('price_discount', 0), item.get('url', ''), item.get('image', ''), item.get('department', ''),
            item.get('category', ''), int(bool(item.get('price'))), guid)

        conn.execute("SELECT EXISTS(SELECT 1 FROM EXTRA_DELIVERY_PRODUCTS WHERE guid = '%s')" % guid)
        ret = conn.fetchone()[0]

        if ret:
            update_stmt = "UPDATE EXTRA_DELIVERY_PRODUCTS SET sku=%d, `name`='%s', price=%f, price_discount=%f, " \
                          "url='%s', image='%s', department='%s', category='%s', `status`=%d WHERE guid='%s'" % \
                          item_data[1:]
            conn.execute(update_stmt)
            spider.logger.debug("Item updated in db: {} {}".format(guid, item))
        else:
            insert_stmt = "INSERT INTO EXTRA_DELIVERY_PRODUCTS (guid, sku, `name`, price, price_discount, url, image," \
                          "department, category, `status`) VALUES ('%s', %d, '%s', %f, %f, '%s', '%s', '%s'," \
                          "'%s', %d)" % item_data[:-1]
            conn.execute(insert_stmt)
            spider.logger.debug("Item stored in db: {} {}".format(guid, item))

    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        # do nothing, just log
        spider.logger.error(failure)

    def _get_guid(self, item):
        """Generates an unique identifier for a given item."""
        # hash based solely in the url field
        return md5(item.get('url').encode()).hexdigest()
