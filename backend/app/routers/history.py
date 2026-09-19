from fastapi import APIRouter, HTTPException
from app.services.metro_service import MetroService

router = APIRouter(tags=["history"])


@router.get("/history")
def history(limit: int = 50):
    with MetroService() as s:
        return {"items": s.history(limit)}


@router.get("/history/{run_id}")
def history_detail(run_id: int):
    with MetroService() as s:
        row = s.run_detail(run_id)
        if not row:
            raise HTTPException(404)
        return row


@router.delete("/history/{run_id}")
def history_delete(run_id: int):
    with MetroService() as s:
        if not s.delete_run(run_id):
            raise HTTPException(404)
        return {"deleted": run_id}
