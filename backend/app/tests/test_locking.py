"""Route-locking behaviour: persisted records freeze the via-station snapshot,
while fresh read-only quotes always recompute against the current graph."""
import pytest

import app.db as db
from app import seed
from app.services.metro_service import MetroService


@pytest.fixture()
def svc(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "test.db")
    seed.init_db()
    with MetroService() as s:
        yield s


def _count(svc):
    return len(svc.history(limit=1000))


def test_persisted_quote_locks_path(svc):
    q = svc.quote("A1", "B2", persist=True)
    assert q["run_id"] is not None
    item = svc.history_item(q["run_id"])
    assert item["result"]["path"] == ["A1", "A2", "B1", "B2"]
    assert item["result"]["hops"] == 3
    assert item["result"]["fare"] == 4.0


def test_locked_record_immune_to_shortcut_edge(svc):
    run_id = svc.quote("A1", "B2", persist=True)["run_id"]

    # Add a shortcut edge on the shortest path: fresh quotes get shorter...
    svc.add_edge("A1", "B2")
    fresh = svc.quote("A1", "B2", persist=False)
    assert fresh["hops"] == 1
    assert fresh["path"] == ["A1", "B2"]
    assert fresh["fare"] == 3.0

    # ...but the locked record keeps its original path, hops and fare.
    locked = svc.history_item(run_id)["result"]
    assert locked["path"] == ["A1", "A2", "B1", "B2"]
    assert locked["hops"] == 3
    assert locked["fare"] == 4.0


def test_locked_record_immune_to_edge_delete(svc):
    run_id = svc.quote("A1", "B2", persist=True)["run_id"]
    svc.remove_edge("B1", "B2")
    svc.remove_edge("A2", "A3")
    assert svc.quote("A1", "B2", persist=False)["reachable"] is False

    locked = svc.history_item(run_id)["result"]
    assert locked["reachable"] is True
    assert locked["path"] == ["A1", "A2", "B1", "B2"]
    assert locked["hops"] == 3


def test_locked_record_immune_to_fare_table_change(svc):
    run_id = svc.quote("A1", "B2", persist=True)["run_id"]
    rules = svc.fare_rules()
    svc.update_fare_rule(rules[1]["id"], 4, 99.0)

    fresh = svc.quote("A1", "B2", persist=False)
    assert fresh["fare"] == 99.0

    locked = svc.history_item(run_id)["result"]
    assert locked["fare"] == 4.0
    assert locked["hops"] == 3


def test_requote_from_record_is_read_only_and_current(svc):
    run_id = svc.quote("A1", "B2", persist=True)["run_id"]
    svc.add_edge("A1", "B2")
    before = _count(svc)

    # Re-quoting from the record must hit the current graph...
    fresh = svc.quote("A1", "B2", persist=False)
    assert fresh["run_id"] is None
    assert fresh["hops"] == 1

    # ...and must NOT write the new path back into the locked record,
    # nor create any new record.
    assert _count(svc) == before
    locked = svc.history_item(run_id)["result"]
    assert locked["path"] == ["A1", "A2", "B1", "B2"]
    assert locked["hops"] == 3


def test_delete_record_keeps_other_records(svc):
    id1 = svc.quote("A1", "B2", persist=True)["run_id"]
    id2 = svc.quote("A1", "A3", persist=True)["run_id"]
    before = svc.history_item(id2)["result"].copy()

    assert svc.delete_run(id1) is True
    assert svc.history_item(id1) is None

    after = svc.history_item(id2)["result"]
    assert after == before
    assert after["path"] == ["A1", "A2", "A3"]


def test_unreachable_quote_not_persisted(svc):
    before = _count(svc)
    q = svc.quote("A1", "Z9", persist=True)
    assert q["run_id"] is None and q["reachable"] is False
    assert _count(svc) == before
