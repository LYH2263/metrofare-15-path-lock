from fastapi import APIRouter, HTTPException

from app.schemas.ops import EdgeRequest
from app.services.metro_service import MetroService

router = APIRouter(tags=["edges"])


@router.get("/edges")
def list_edges():
    with MetroService() as s:
        return {"items": s.edges()}


@router.post("/edges", status_code=201)
def add_edge(body: EdgeRequest):
    if body.a == body.b:
        raise HTTPException(400, "self loop not allowed")
    with MetroService() as s:
        if not s.add_edge(body.a, body.b):
            raise HTTPException(409, "edge already exists")
        return {"a": body.a, "b": body.b}


@router.delete("/edges")
def remove_edge(a: str, b: str):
    with MetroService() as s:
        if not s.remove_edge(a, b):
            raise HTTPException(404, "edge not found")
        return {"deleted": {"a": a, "b": b}}
