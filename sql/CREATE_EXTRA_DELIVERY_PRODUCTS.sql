DROP TABLE IF EXISTS EXTRA_DELIVERY_PRODUCTS;

CREATE TABLE EXTRA_DELIVERY_PRODUCTS
(
  guid           CHAR(32)  NOT NULL PRIMARY KEY,
  CONSTRAINT guid_uindex UNIQUE (guid),
  sku            INT,
  `name`         TEXT,
  price          FLOAT,
  price_discount FLOAT,
  url            TEXT,
  image          TEXT,
  department     VARCHAR(255),
  category       VARCHAR(255),
  `status`       TINYINT(1),
  created_at     TIMESTAMP NOT NULL             DEFAULT CURRENT_TIMESTAMP,
  updated_at     TIMESTAMP NOT NULL             DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);