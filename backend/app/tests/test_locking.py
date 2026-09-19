"""途经锁定：写入记录锁快照；增删边、改票价表不影响已锁记录；只读试算走当前图。"""
import os
import tempfile

os.environ["DATA_DIR"] = tempfile.mkdtemp(prefix="metrofare-test-")

from app import seed  # noqa: E402
from app.services.metro_service import MetroService  # noqa: E402

seed.init_db()


def test_locked_snapshot_survives_graph_and_fare_changes():
    with MetroService() as s:
        # 写入成功 → 途经/站数/票价锁进快照
        q = s.quote("A1", "B2", True)
        rid = q["run_id"]
        assert rid is not None
        assert q["path"] == ["A1", "A2", "B1", "B2"]
        assert q["hops"] == 3 and q["fare"] == 4.0

        # 在最短路上新增捷径边 → 当场只读试算站数变短，且不写记录
        s.add_edge("A2", "B2")
        live = s.quote("A1", "B2", False)
        assert live["run_id"] is None
        assert live["hops"] == 2
        assert live["path"] == ["A1", "A2", "B2"]

        # 改票价表（2 站那档）→ 当场试算票价变，锁定记录不变
        assert s.update_fare_rule(1, 2, 99.0)
        assert s.quote("A1", "B2", False)["fare"] == 99.0

        locked = s.run_detail(rid)
        assert locked["hops"] == 3
        assert locked["fare"] == 4.0
        assert locked["path"] == ["A1", "A2", "B1", "B2"]

        # 删边后锁定记录依旧不变
        assert s.remove_edge("A2", "B2")
        assert s.run_detail(rid)["hops"] == 3

        # 删除该锁定记录 → 其他记录（种子 #1）途经不变
        seeded_before = s.run_detail(1)
        assert seeded_before["path"] == ["A1", "A2", "A3"]
        assert s.delete_run(rid) is True
        assert s.run_detail(rid) is None
        assert s.delete_run(rid) is False
        assert s.run_detail(1) == seeded_before


def test_readonly_quote_never_writes():
    with MetroService() as s:
        before = len(s.history())
        assert s.quote("A1", "A3", False)["run_id"] is None
        assert len(s.history()) == before


def test_unreachable_quote_not_persisted():
    with MetroService() as s:
        before = len(s.history())
        q = s.quote("A1", "ZZ", True)
        assert q["run_id"] is None and q["reachable"] is False
        assert len(s.history()) == before
