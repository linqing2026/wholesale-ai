#!/usr/bin/env python3
"""批发助手 · 四大能力模块查询引擎"""
import sqlite3, sys, os

DB = os.path.expanduser("~/.openclaw/wholesale.db")

def connect():
    return sqlite3.connect(DB)

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
def _match_wine(keyword):
    """智能匹配酒款，支持'82拉菲'→拉菲1982, '2015茅台'→茅台2015"""
    import re
    conn = connect()
    cur = conn.cursor()
    # 提取可能的年份前缀
    yr_match = re.match(r'(\d{2,4})(.+)', keyword)
    if yr_match:
        yr, name = yr_match.group(1), yr_match.group(2)
        if len(yr) == 2:
            yr = '19' + yr if int(yr) > 50 else '20' + yr
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

def profit_calculator(wine_keyword, sell_price):
    matches = _match_wine(wine_keyword)
    if not matches:
        return f"❌ 未找到酒款: {wine_keyword}"
    results = []
    for name, vintage, cost, supplier in matches:
        total_cost = cost * 1.15  # 进价 + 15% 综合成本
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
    rows.sort(key=lambda r: r[2])  # 按进价升序
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
    # 呆滞品：库存 > 安全库存*2 且 90 天无采购
    cur.execute("""
        SELECT w.name, w.vintage, i.quantity, w.safety_stock,
               w.cost_price * i.quantity AS capital
        FROM wines w
        JOIN inventory i ON w.id = i.wine_id
        WHERE i.quantity > w.safety_stock * 2
        ORDER BY capital DESC
    """)
    stale = cur.fetchall()
    # 资金占用 TOP5
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

# ── CLI ──
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: query_db.py <模块> [参数]")
        print("模块: procurement | profit <酒款> <售价> | compare <酒款> | scanner")
        sys.exit(1)
    module = sys.argv[1]
    if module == "procurement":
        print(procurement_advisor())
    elif module == "profit":
        if len(sys.argv) < 4:
            print("用法: query_db.py profit <酒款名> <售价>")
        else:
            print(profit_calculator(sys.argv[2], float(sys.argv[3])))
    elif module == "compare":
        if len(sys.argv) < 3:
            print("用法: query_db.py compare <酒款名>")
        else:
            print(supplier_compare(sys.argv[2]))
    elif module == "scanner":
        print(inventory_scanner())
    else:
        print(f"未知模块: {module}")
