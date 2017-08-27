# -*- coding: utf-8 -*-

BOT_NAME = 'smartcart'

SPIDER_MODULES = ['smartcart.spiders']
NEWSPIDER_MODULE = 'smartcart.spiders'

ROBOTSTXT_OBEY = False

TELNETCONSOLE_ENABLED = False

DUPEFILTER_DEBUG = True

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
}

FAKEUSERAGENT_FALLBACK = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                         'Chrome/41.0.2228.0 Safari/537.36'

EXTENSIONS = {
    'scrapy.extensions.telnet.TelnetConsole': None,
}

ITEM_PIPELINES = {
    'scrapy_mongodb.MongoDBPipeline': 300,
    # 'smartcart.pipelines.SmartCartMySQLPipeline': 300,
}

MONGODB_URI = 'mongodb://localhost:27017'
MONGODB_DATABASE = 'smartcart'
MONGODB_UNIQUE_KEY = 'url'
MONGODB_ADD_TIMESTAMP = True
MONGODB_SEPARATE_COLLECTIONS = True

# MYSQL_HOST = ''
# MYSQL_DBNAME = ''
# MYSQL_USER = ''
# MYSQL_PASSWD = ''

CONCURRENT_REQUESTS = 32
CONCURRENT_REQUESTS_PER_DOMAIN = 32

DOWNLOAD_DELAY = 0.3

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 32
AUTOTHROTTLE_DEBUG = True

FEED_EXPORT_ENCODING = 'utf-8'
