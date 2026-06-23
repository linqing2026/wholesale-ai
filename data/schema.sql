-- 批发AI助手 · 数据库建表脚本
-- 使用: sqlite3 wholesale.db < schema.sql

CREATE TABLE IF NOT EXISTS suppliers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    contact_person TEXT,
    phone TEXT,
    payment_terms TEXT
);

CREATE TABLE IF NOT EXISTS wines (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    vintage INTEGER,
    spec TEXT,
    supplier_id INTEGER REFERENCES suppliers(id),
    cost_price REAL NOT NULL,
    safety_stock INTEGER DEFAULT 5
);

CREATE TABLE IF NOT EXISTS inventory (
    wine_id INTEGER REFERENCES wines(id),
    quantity INTEGER DEFAULT 0,
    warehouse TEXT DEFAULT '主仓',
    updated_at TEXT DEFAULT (date('now'))
);

CREATE TABLE IF NOT EXISTS purchase_orders (
    id INTEGER PRIMARY KEY,
    wine_id INTEGER REFERENCES wines(id),
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    supplier_id INTEGER REFERENCES suppliers(id),
    purchased_at TEXT DEFAULT (datetime('now'))
);

-- 示例数据
INSERT OR IGNORE INTO suppliers VALUES (1, '华盛酒业', '老王', '13800001111', '月结30天');
INSERT OR IGNORE INTO suppliers VALUES (2, '国酒商贸', '张总', '13800002222', '现结');
INSERT OR IGNORE INTO suppliers VALUES (3, '洋酒国际', 'Lisa', '13800003333', '月结45天');
INSERT OR IGNORE INTO suppliers VALUES (4, '澳酒直供', 'Jack', '13800004444', '款到发货');

INSERT OR IGNORE INTO wines VALUES (1, '拉菲', 1982, '750ml×6', 1, 4200, 5);
INSERT OR IGNORE INTO wines VALUES (2, '拉菲', 2015, '750ml×6', 1, 2800, 5);
INSERT OR IGNORE INTO wines VALUES (3, '茅台', 2015, '500ml×6', 2, 3800, 5);
INSERT OR IGNORE INTO wines VALUES (4, '茅台', 2020, '500ml×6', 2, 2600, 5);
INSERT OR IGNORE INTO wines VALUES (5, '轩尼诗XO', 2018, '700ml×6', 3, 2200, 5);
INSERT OR IGNORE INTO wines VALUES (6, '马爹利蓝带', 2019, '700ml×6', 3, 1800, 5);
INSERT OR IGNORE INTO wines VALUES (7, '奔富407', 2018, '750ml×6', 4, 900, 5);
INSERT OR IGNORE INTO wines VALUES (8, '五粮液', 2021, '500ml×6', 2, 600, 5);

INSERT OR IGNORE INTO inventory VALUES (1, 8, '主仓', '2026-06-23');
INSERT OR IGNORE INTO inventory VALUES (2, 15, '主仓', '2026-06-23');
INSERT OR IGNORE INTO inventory VALUES (3, 3, '主仓', '2026-06-23');
INSERT OR IGNORE INTO inventory VALUES (4, 12, '主仓', '2026-06-23');
INSERT OR IGNORE INTO inventory VALUES (5, 6, '主仓', '2026-06-23');
INSERT OR IGNORE INTO inventory VALUES (6, 10, '主仓', '2026-06-23');
INSERT OR IGNORE INTO inventory VALUES (7, 20, '主仓', '2026-06-23');
INSERT OR IGNORE INTO inventory VALUES (8, 25, '主仓', '2026-06-23');
