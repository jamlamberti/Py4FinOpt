CREATE SCHEMA IF NOT EXISTS `pyfinopt` DEFAULT CHARACTER SET utf8 COLLATE utf8_bin;

USE pyfinopt;

DROP TABLE IF EXISTS `dailyCacheStocks`;

CREATE TABLE IF NOT EXISTS `dailyCacheStocks`(
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
    `ticker` VARCHAR(7) NOT NULL,
    `timestamp` DATE NOT NULL,
    `open` DOUBLE(8,2), -- Thanks to BRK-A
    `high` DOUBLE(8,2),
    `low` DOUBLE(8,2),
    `close` DOUBLE(8,2),
    `volume` INT(11) UNSIGNED NOT NULL,
    `adjclose` DOUBLE(8,2),
    PRIMARY KEY(`id`),
    CONSTRAINT uc_ticker_tstamp UNIQUE (ticker, timestamp)
);


