# Smart Cart

### About

O projeto Smart Cart contém crawlers que obtém dados de sites populares de varejo brasileiro, acessando os domínios, procurando por departamentos/categorias e catalogando todos os produtos encontrados.

Foi desenvolvido em Python 3.6 utilizando a biblioteca Scrapy.

<img src="https://www.python.org/static/opengraph-icon-200x200.png" alt="Python" style="width: 200px;"/>
<img src="https://scrapinghub.files.wordpress.com/2016/08/scrapy.png" alt="Scrapy" style="width: 150px;"/>

#### Requirements

* [Python 3.6](https://www.python.org/downloads/release/python-360/)
* [scrapy](https://github.com/scrapy/scrapy)
* [scrapy-fake-useragent](https://github.com/alecxe/scrapy-fake-useragent)
* [shub](https://github.com/scrapinghub/shub)
* [mysqlclient](https://github.com/PyMySQL/mysqlclient-python)

#### Install

```shell
pip install virtualenv
virtualenv sc-env
source sc-env/bin/activate

cd smartcart
pip install -r requirements.txt
```

### Run

##### Local

```shell
python main.py
```

##### Cloud

```shell
shub login
shub deploy
```

### Config

As configurações do projeto se encontram no arquivo settings.py. Nesse arquivo é possível modificar informações como o banco de dados utilizado, user agent, throttling, concorrência entre outras. Uma lista com todas as configurações pode ser encontrada na [documentação oficial do Scrapy](https://doc.scrapy.org/en/latest/topics/settings.html). Também é possível informar as configurações pela [linha de comando](https://doc.scrapy.org/en/latest/topics/settings.html#command-line-options).

##### DB

No momento o crawler oferece suporte ao banco de dados MySQL, implementando uma pipeline que realiza a conexão e o salvamento dos itens no banco informado nas seguintes configurações no settings.py:

```python
ITEM_PIPELINES = {
   'smartcart.pipelines.ExtraDeliveryMySQLPipeline': 300,
}

MYSQL_HOST = 'host'
MYSQL_DBNAME = 'db_name'
MYSQL_USER = 'db_user'
MYSQL_PASSWD = 'db_pass'
```

A biblioteca também oferece export dos dados nos formatos [JSON, XML e CSV](https://doc.scrapy.org/en/latest/topics/feed-exports.html).

##### Performance

O crawler pode ser configurado para coletar os dados do site mais rapidamente, porém isso pode causar a detecção do bot e seu possível banimento. As principais configurações que controlam esse aspecto são:

```python
CONCURRENT_REQUESTS = 32

DOWNLOAD_DELAY = 0.3
CONCURRENT_REQUESTS_PER_DOMAIN = 16

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 32
AUTOTHROTTLE_DEBUG = True
```

As configurações de autothrottle aplicam o delay entre requests do crawler. Com essa opção ativada, o bot automaticamente ajusta esse delay para causar menos stress no site crawleado e evitar detecção, ao custo de demorar mais para finalizar o crawl.

---
