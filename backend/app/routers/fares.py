from fastapi import APIRouter, HTTPException

from app.schemas.ops import FareRuleRequest
from app.services.metro_service import MetroService

router = APIRouter(tags=["fares"])


@router.get("/fare-rules")
def fare_rules():
    with MetroService() as s:
        return {"items": s.fare_rules()}


@router.post("/fare-rules", status_code=201)
def add_fare_rule(body: FareRuleRequest):
    with MetroService() as s:
        rule_id = s.add_fare_rule(body.max_hops, body.price)
        return {"id": rule_id, "max_hops": body.max_hops, "price": body.price}


@router.put("/fare-rules/{rule_id}")
def update_fare_rule(rule_id: int, body: FareRuleRequest):
    with MetroService() as s:
        if not s.update_fare_rule(rule_id, body.max_hops, body.price):
            raise HTTPException(404, "fare rule not found")
        return {"id": rule_id, "max_hops": body.max_hops, "price": body.price}


@router.delete("/fare-rules/{rule_id}")
def delete_fare_rule(rule_id: int):
    with MetroService() as s:
        if not s.delete_fare_rule(rule_id):
            raise HTTPException(404, "fare rule not found")
        return {"deleted": rule_id}
