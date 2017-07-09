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

# ITEM_PIPELINES = {
#    'smartcart.pipelines.ExtraDeliveryMySQLPipeline': 300,
# }

# MYSQL_HOST = 'sql10.freemysqlhosting.net'
# MYSQL_DBNAME = 'sql10184422'
# MYSQL_USER = 'sql10184422'
# MYSQL_PASSWD = 'f26Gx8MDu3'

# dkn65223@tqosi.com mA6^0MyIi&OB7lS8cL1lTc

CONCURRENT_REQUESTS = 32
CONCURRENT_REQUESTS_PER_DOMAIN = 32

DOWNLOAD_DELAY = 0.3

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 32
AUTOTHROTTLE_DEBUG = True

FEED_EXPORT_ENCODING = 'utf-8'

