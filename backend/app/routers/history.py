from fastapi import APIRouter, HTTPException

from app.services.metro_service import MetroService

router = APIRouter(tags=["history"])


@router.get("/history")
def history(limit: int = 50):
    with MetroService() as s:
        return {"items": s.history(limit)}


@router.get("/history/{run_id}")
def history_item(run_id: int):
    """Open one record by id: returns the locked snapshot verbatim (no recompute)."""
    with MetroService() as s:
        item = s.history_item(run_id)
        if item is None:
            raise HTTPException(404, "record not found")
        return item


@router.delete("/history/{run_id}")
def delete_history_item(run_id: int):
    """Delete one record; other records' snapshots are untouched."""
    with MetroService() as s:
        if not s.delete_run(run_id):
            raise HTTPException(404, "record not found")
        return {"deleted": run_id}
