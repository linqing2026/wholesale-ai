#!/usr/bin/env python3
"""批发助手 · 六大模块引擎（出货+入库+四大查询）"""
import sqlite3, sys, os, re

DB = os.path.expanduser("~/.openclaw/wholesale.db")

def connect():
    return sqlite3.connect(DB)

def _parse_year(keyword):
    """智能解析年份：'82拉菲' → (name='拉菲', year='1982'), '茅台2015' → (name='茅台', year='2015')"""
    # 年份前缀：82拉菲
    m = re.match(r'(\d{2,4})(.+)', keyword)
    if m and re.match(r'^\d+$', m.group(1)):
        yr, name = m.group(1), m.group(2)
        if len(yr) == 2:
            yr = '19' + yr if int(yr) > 50 else '20' + yr
        return name.strip(), yr
    # 年份后缀：茅台2015
    m = re.match(r'(.+?)(\d{2,4})$', keyword)
    if m:
        name, yr = m.group(1), m.group(2)
        if len(yr) == 2:
            yr = '19' + yr if int(yr) > 50 else '20' + yr
        return name.strip(), yr
    return keyword, None

# ── 酒款匹配 ──
def _match_wine(keyword):
    conn = connect()
    cur = conn.cursor()
    name, yr = _parse_year(keyword)
    if yr:
        cur.execute(
            "SELECT w.name, w.vintage, w.cost_price, s.name FROM wines w LEFT JOIN suppliers s ON w.supplier_id=s.id WHERE w.name LIKE ? AND CAST(w.vintage AS TEXT) LIKE ?",
            (f"%{name}%", f"%{yr}%"))
        rows = cur.fetchall()
        if rows: conn.close(); return rows
    cur.execute(
        "SELECT w.name, w.vintage, w.cost_price, s.name FROM wines w LEFT JOIN suppliers s ON w.supplier_id=s.id WHERE w.name LIKE ?",
        (f"%{keyword}%",))
    rows = cur.fetchall()
    conn.close()
    return rows

def _match_wine_with_id(keyword):
    conn = connect()
    cur = conn.cursor()
    name, yr = _parse_year(keyword)
    if yr:
        cur.execute(
            "SELECT w.id, w.name, w.vintage, w.cost_price, s.name FROM wines w LEFT JOIN suppliers s ON w.supplier_id=s.id WHERE w.name LIKE ? AND CAST(w.vintage AS TEXT) LIKE ?",
            (f"%{name}%", f"%{yr}%"))
        rows = cur.fetchall()
        if rows: conn.close(); return rows
    cur.execute(
        "SELECT w.id, w.name, w.vintage, w.cost_price, s.name FROM wines w LEFT JOIN suppliers s ON w.supplier_id=s.id WHERE w.name LIKE ?",
        (f"%{keyword}%",))
    rows = cur.fetchall()
    conn.close()
    return rows

def _ensure_type_column():
    try:
        conn = connect()
        conn.execute("ALTER TABLE purchase_orders ADD COLUMN type TEXT DEFAULT 'purchase'")
        conn.commit()
        conn.close()
    except:
        pass

# ── 模块 1：采购参谋 ──
def procurement_advisor():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT w.name, w.vintage, w.safety_stock, i.quantity,
               MAX(w.safety_stock * 2 - i.quantity, 0) AS suggest_buy
        FROM wines w
        JOIN inventory i ON w.id = i.wine_id
        WHERE i.quantity <= w.safety_stock
        ORDER BY i.quantity ASC
    """)
    rows = cur.fetchall()
    conn.close()
    if not rows:
        return "✅ 所有酒款库存充足，无需补货"
    lines = ["📦 补货建议"]
    for name, vintage, safety, qty, suggest in rows:
        lines.append(f"  {name} {vintage} · 库存{qty}箱 · 安全水位{safety}箱 · 建议补{suggest}箱")
    return "\n".join(lines)

# ── 模块 2：利润精算师 ──
def profit_calculator(wine_keyword, sell_price):
    matches = _match_wine(wine_keyword)
    if not matches:
        return f"❌ 未找到酒款: {wine_keyword}"
    results = []
    for name, vintage, cost, supplier in matches:
        total_cost = cost * 1.15
        margin = sell_price - total_cost
        margin_pct = margin / sell_price * 100
        flag = "🟢" if margin_pct > 20 else ("🟡" if margin_pct > 10 else "🔴")
        results.append(
            f"{flag} {name} {vintage} · 进价¥{cost:.0f} · 综合成本¥{total_cost:.0f} · "
            f"售¥{sell_price:.0f} → 毛利{margin_pct:.1f}% (¥{margin:.0f}/箱)"
        )
    return "\n".join(results)

# ── 模块 3：供应商比价 ──
def supplier_compare(wine_keyword):
    rows = _match_wine(wine_keyword)
    if not rows:
        return f"❌ 未找到酒款: {wine_keyword}"
    rows.sort(key=lambda r: r[2])
    lines = [f"📊 {wine_keyword} 供应商比价"]
    cheapest = rows[0]
    for name, vintage, price, supplier in rows:
        diff = price - cheapest[2]
        tag = " ← 最低" if diff == 0 else f" (+¥{diff:.0f})"
        lines.append(f"  {supplier} · ¥{price:.0f}/箱{tag}")
    return "\n".join(lines)

# ── 模块 4：库存健康扫描 ──
def inventory_scanner():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT w.name, w.vintage, i.quantity, w.safety_stock,
               w.cost_price * i.quantity AS capital
        FROM wines w
        JOIN inventory i ON w.id = i.wine_id
        WHERE i.quantity > w.safety_stock * 2
        ORDER BY capital DESC
    """)
    stale = cur.fetchall()
    cur.execute("""
        SELECT w.name, w.vintage, i.quantity, w.cost_price,
               w.cost_price * i.quantity AS capital
        FROM wines w
        JOIN inventory i ON w.id = i.wine_id
        ORDER BY capital DESC
        LIMIT 5
    """)
    top5 = cur.fetchall()
    conn.close()
    lines = []
    if stale:
        lines.append("⚠️ 呆滞品（库存超安全水位2倍）")
        for name, vintage, qty, safety, capital in stale:
            lines.append(f"  {name} {vintage} · 库存{qty}箱(安全{safety}) · 占用¥{capital:,.0f}")
    else:
        lines.append("✅ 无呆滞品")
    lines.append("")
    lines.append("💰 资金占用 TOP5")
    for i, (name, vintage, qty, cost, capital) in enumerate(top5, 1):
        lines.append(f"  {i}. {name} {vintage} · {qty}箱×¥{cost:.0f} = ¥{capital:,.0f}")
    return "\n".join(lines)

# ── 模块 5：出货登记 ──
def record_sale(wine_keyword, quantity, sell_price):
    matches = _match_wine_with_id(wine_keyword)
    if not matches:
        return f"❌ 未找到酒款: {wine_keyword}"
    wine_id, name, vintage, cost, supplier = matches[0]

    _ensure_type_column()
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT quantity FROM inventory WHERE wine_id=?", (wine_id,))
    row = cur.fetchone()
    current_qty = row[0] if row else 0
    if current_qty < quantity:
        conn.close()
        return f"❌ 库存不足: {name} {vintage} · 当前{current_qty}箱 · 需要{quantity}箱"

    new_qty = current_qty - quantity
    cur.execute("UPDATE inventory SET quantity=?, updated_at=date('now') WHERE wine_id=?", (new_qty, wine_id))
    cur.execute(
        "INSERT INTO purchase_orders (wine_id, quantity, unit_price, supplier_id, purchased_at, type) VALUES (?,?,?,?,datetime('now'),'sale')",
        (wine_id, quantity, sell_price, matches[0][4] if matches[0][4] else None))

    total_cost = cost * 1.15
    margin = sell_price - total_cost
    margin_pct = margin / sell_price * 100
    flag = "🟢" if margin_pct > 20 else ("🟡" if margin_pct > 10 else "🔴")

    conn.commit()
    conn.close()
    return (
        f"✅ 已出货: {name} {vintage} ×{quantity}箱 @¥{sell_price:.0f}\n"
        f"   库存: {current_qty} → {new_qty}箱\n"
        f"   {flag} 毛利{margin_pct:.1f}% (¥{margin*quantity:.0f})"
    )

# ── 模块 6：入库登记 ──
def record_restock(wine_keyword, quantity, cost_price=None):
    matches = _match_wine_with_id(wine_keyword)
    if not matches:
        return f"❌ 未找到酒款: {wine_keyword}"
    wine_id, name, vintage, old_cost, supplier = matches[0]
    if cost_price is None:
        cost_price = old_cost

    _ensure_type_column()
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT quantity FROM inventory WHERE wine_id=?", (wine_id,))
    row = cur.fetchone()
    current_qty = row[0] if row else 0
    new_qty = current_qty + quantity
    cur.execute("UPDATE inventory SET quantity=?, updated_at=date('now') WHERE wine_id=?", (new_qty, wine_id))
    cur.execute(
        "INSERT INTO purchase_orders (wine_id, quantity, unit_price, supplier_id, purchased_at, type) VALUES (?,?,?,?,datetime('now'),'purchase')",
        (wine_id, quantity, cost_price, matches[0][4] if matches[0][4] else None))

    if cost_price != old_cost:
        cur.execute("UPDATE wines SET cost_price=? WHERE id=?", (cost_price, wine_id))

    conn.commit()
    conn.close()
    msg = f"✅ 已入库: {name} {vintage} ×{quantity}箱 @¥{cost_price:.0f}/箱\n   库存: {current_qty} → {new_qty}箱"
    if cost_price != old_cost:
        msg += f"\n   ⚠️ 进价变更: ¥{old_cost:.0f} → ¥{cost_price:.0f}"
    return msg

# ── CLI ──
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("六大模块: procurement | profit <酒> <价> | compare <酒> | scanner | sell <酒> <量> <价> | restock <酒> <量> [价]")
        sys.exit(1)
    m = sys.argv[1]
    if m == "procurement":
        print(procurement_advisor())
    elif m == "profit":
        print(profit_calculator(sys.argv[2], float(sys.argv[3])))
    elif m == "compare":
        print(supplier_compare(sys.argv[2]))
    elif m == "scanner":
        print(inventory_scanner())
    elif m == "sell":
        print(record_sale(sys.argv[2], int(sys.argv[3]), float(sys.argv[4])))
    elif m == "restock":
        cost = float(sys.argv[4]) if len(sys.argv) >= 5 else None
        print(record_restock(sys.argv[2], int(sys.argv[3]), cost))
    else:
        print(f"未知模块: {m}")
