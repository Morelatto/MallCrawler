# Mall Crawler

### About

O projeto Mall Crawler foi desenvolvido com o objetivo de obter os dados dos sites mais populares de varejo no Brasil. 
O bot acessa os domínios navegando por departamentos ou categorias e registra todos os produtos encontrados.
Foi desenvolvido em Python utilizando a biblioteca Scrapy.

#### Requirements

* Python
* [Scrapy](https://github.com/scrapy/scrapy)
* [Scrapinghub Command Line Client](https://github.com/scrapinghub/shub)
* MySQL
* [mysqlclient](https://github.com/PyMySQL/mysqlclient-python)

#### Install

```shell
pip install virtualenv
virtualenv venv
source venv/bin/activate

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

O arquivo settings.py contém as configurações principais do projeto e nele é possível configurar diversas opções como banco de dados, User Agent, throttling, concorrência entre outras. 
Uma lista com todas as configurações pode ser encontrada na [documentação oficial do Scrapy](https://doc.scrapy.org/en/latest/topics/settings.html). 
Também é possível informar as configurações pela [linha de comando](https://doc.scrapy.org/en/latest/topics/settings.html#command-line-options).

##### DB

No momento o crawler oferece suporte ao banco de dados MySQL por meio do pipeline que realiza a conexão e persistência dos itens no banco.
As seguintes configurações de banco podem ser alteradas:

```python
MYSQL_HOST = ''
MYSQL_DBNAME = ''
MYSQL_USER = ''
MYSQL_PASSWD = ''
```

O Scrapy também oferece export dos dados nos formatos [JSON, XML e CSV](https://doc.scrapy.org/en/latest/topics/feed-exports.html).

##### Performance

O crawler pode ser ajustado para coletar os dados de forma mais agressiva, porém as chances de detecção e bloqueio consequentemente aumentam.
As principais opções abaixo controlam a performance do bot:

```python
CONCURRENT_REQUESTS_PER_DOMAIN = 16
DOWNLOAD_DELAY = 0.3

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_DEBUG = True
```

A lib fornece uma extensão de AutoThrottle com o objetivo de diminuir o impacto nos domínios, e suas configurações aplicam um delay dinâmico entre requests. 

