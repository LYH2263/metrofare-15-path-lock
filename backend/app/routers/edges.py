from fastapi import APIRouter, HTTPException
from app.schemas.edges import EdgeIn
from app.services.metro_service import MetroService

router = APIRouter(tags=["edges"])


@router.get("/edges")
def list_edges():
    with MetroService() as s:
        return {"items": s.edges()}


@router.post("/edges")
def add_edge(body: EdgeIn):
    if body.a == body.b:
        raise HTTPException(400, "self loop")
    with MetroService() as s:
        s.add_edge(body.a, body.b)
        return {"items": s.edges()}


@router.delete("/edges")
def remove_edge(body: EdgeIn):
    with MetroService() as s:
        if not s.remove_edge(body.a, body.b):
            raise HTTPException(404)
        return {"items": s.edges()}
