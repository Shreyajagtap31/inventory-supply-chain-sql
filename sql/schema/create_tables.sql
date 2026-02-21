CREATE TABLE IF NOT EXISTS products (
    sku_id          VARCHAR PRIMARY KEY,
    product_name    VARCHAR,
    category        VARCHAR,
    supplier_id     VARCHAR,
    lead_time_days  INTEGER,
    reorder_point   INTEGER,
    unit_cost       DECIMAL(10,2)
);

CREATE TABLE IF NOT EXISTS inventory (
    sku_id        VARCHAR PRIMARY KEY,
    stock_level   INTEGER,
    warehouse     VARCHAR,
    last_updated  DATE
);

CREATE TABLE IF NOT EXISTS sales_history (
    sku_id      VARCHAR,
    sale_date   DATE,
    quantity    INTEGER,
    unit_cost   DECIMAL(10,2)
);

CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id       VARCHAR PRIMARY KEY,
    supplier_name     VARCHAR,
    reliability_score DECIMAL(4,2),
    avg_lead_time     INTEGER
);

CREATE TABLE IF NOT EXISTS purchase_orders (
    order_id       VARCHAR PRIMARY KEY,
    sku_id         VARCHAR,
    order_date     DATE,
    order_quantity INTEGER,
    supplier_id    VARCHAR
);