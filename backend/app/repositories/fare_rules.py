import sqlite3


def list_ordered(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute("SELECT id, max_hops, price FROM fare_rules ORDER BY id").fetchall()
    return [dict(r) for r in rows]


def as_calc_rules(conn: sqlite3.Connection) -> list[dict]:
    return [{"max_hops": r["max_hops"], "price": r["price"]} for r in list_ordered(conn)]


def insert(conn: sqlite3.Connection, max_hops: int | None, price: float) -> int:
    cur = conn.execute(
        "INSERT INTO fare_rules(max_hops, price) VALUES (?,?)", (max_hops, price)
    )
    conn.commit()
    return int(cur.lastrowid)


def update(conn: sqlite3.Connection, rule_id: int, max_hops: int | None, price: float) -> bool:
    cur = conn.execute(
        "UPDATE fare_rules SET max_hops=?, price=? WHERE id=?", (max_hops, price, rule_id)
    )
    conn.commit()
    return cur.rowcount > 0


def delete(conn: sqlite3.Connection, rule_id: int) -> bool:
    cur = conn.execute("DELETE FROM fare_rules WHERE id=?", (rule_id,))
    conn.commit()
    return cur.rowcount > 0
