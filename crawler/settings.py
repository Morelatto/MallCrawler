# -*- coding: utf-8 -*-

BOT_NAME = 'mall_crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'

ROBOTSTXT_OBEY = False

TELNETCONSOLE_ENABLED = False
EXTENSIONS = {
    'scrapy.extensions.telnet.TelnetConsole': None,
}

DUPEFILTER_DEBUG = True

ITEM_PIPELINES = {
    'smartcart.pipelines.SmartCartMySQLPipeline': 300,
}

MYSQL_HOST = ''
MYSQL_DBNAME = ''
MYSQL_USER = ''
MYSQL_PASSWD = ''

CONCURRENT_REQUESTS_PER_DOMAIN = 32

DOWNLOAD_DELAY = 0.3

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_DEBUG = True

FEED_EXPORT_ENCODING = 'utf-8'
