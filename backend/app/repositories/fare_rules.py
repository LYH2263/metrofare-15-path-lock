import sqlite3


def list_ordered(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute("SELECT id, max_hops, price FROM fare_rules ORDER BY id").fetchall()
    return [dict(r) for r in rows]


def as_calc_rules(conn: sqlite3.Connection) -> list[dict]:
    return [{"max_hops": r["max_hops"], "price": r["price"]} for r in list_ordered(conn)]


def update(conn: sqlite3.Connection, rule_id: int, max_hops: int | None, price: float) -> bool:
    cur = conn.execute(
        "UPDATE fare_rules SET max_hops=?, price=? WHERE id=?", (max_hops, price, rule_id)
    )
    conn.commit()
    return cur.rowcount > 0
