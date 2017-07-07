CREATE TABLE EXTRA_DELIVERY_PRODUCTS
(
    guid CHAR(32) NOT NULL PRIMARY KEY,
    CONSTRAINT EXTRA_DELIVERY_PRODUCTS_guid_uindex UNIQUE (guid),
    sku INT,
    `name` TEXT,
    department VARCHAR(255),
    category VARCHAR(255),
    price FLOAT,
    price_discount FLOAT,
    `status` TINYINT(1),
    url TEXT,
    image TEXT,
    updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
)