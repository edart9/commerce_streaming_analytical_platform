CREATE SCHEMA IF NOT EXISTS replica;
CREATE SCHEMA IF NOT EXISTS cubos;
CREATE SCHEMA IF NOT EXISTS audit;

CREATE TABLE IF NOT EXISTS replica.t_ecommerce_events (
    event_time     TIMESTAMP(3),
    event_type     VARCHAR,
    product_id     BIGINT,
    category_id    BIGINT,
    category_code  VARCHAR,
    brand          VARCHAR,
    price          DOUBLE PRECISION,
    user_id        BIGINT,
    user_session   VARCHAR,
    ip             VARCHAR,
    proctime       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
