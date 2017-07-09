#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scrapy import cmdline

# cmdline.execute("scrapy crawl extra_delivery -o result_extra.json".split())
cmdline.execute("scrapy crawl sonda_delivery -o result_sonda.json".split())
