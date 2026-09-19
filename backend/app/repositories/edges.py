import sqlite3


def list_pairs(conn: sqlite3.Connection) -> list[tuple[str, str]]:
    return [(r["a"], r["b"]) for r in conn.execute("SELECT a,b FROM edges").fetchall()]


def add_pair(conn: sqlite3.Connection, a: str, b: str) -> None:
    """Insert undirected edge once, regardless of stored orientation."""
    hit = conn.execute(
        "SELECT 1 FROM edges WHERE (a=? AND b=?) OR (a=? AND b=?)", (a, b, b, a)
    ).fetchone()
    if not hit:
        conn.execute("INSERT INTO edges(a,b) VALUES (?,?)", (a, b))
        conn.commit()


def remove_pair(conn: sqlite3.Connection, a: str, b: str) -> bool:
    cur = conn.execute(
        "DELETE FROM edges WHERE (a=? AND b=?) OR (a=? AND b=?)", (a, b, b, a)
    )
    conn.commit()
    return cur.rowcount > 0
