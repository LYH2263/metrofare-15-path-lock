from fastapi import APIRouter, HTTPException
from app.schemas.fares import FareRuleIn
from app.services.metro_service import MetroService

router = APIRouter(tags=["fares"])


@router.get("/fare-rules")
def fare_rules():
    with MetroService() as s:
        return {"items": s.fare_rules()}


@router.put("/fare-rules/{rule_id}")
def update_fare_rule(rule_id: int, body: FareRuleIn):
    with MetroService() as s:
        if not s.update_fare_rule(rule_id, body.max_hops, body.price):
            raise HTTPException(404)
        return {"items": s.fare_rules()}
