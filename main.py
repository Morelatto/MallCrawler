#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from scrapy import cmdline

# cmdline.execute("scrapy crawl extra_delivery -o result_extra.json".split())
# cmdline.execute("scrapy crawl sonda_delivery -o result_sonda.json".split())
cmdline.execute("scrapy crawl pao_de_acucar -o result_paodeacucar.json".split())
