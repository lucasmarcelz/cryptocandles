CREATE TABLE candlestick
(
    id          INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    currency_name VARCHAR(10)       NOT NULL,
    frequency   TINYINT         NOT NULL,
    datetime    DATETIME        NOT NULL,
    open        DECIMAL(20, 10) NOT NULL,
    high        DECIMAL(20, 10) NOT NULL,
    low         DECIMAL(20, 10) NOT NULL,
    close       DECIMAL(20, 10) NOT NULL

)