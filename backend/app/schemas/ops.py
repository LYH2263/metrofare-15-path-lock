from pydantic import BaseModel


class EdgeRequest(BaseModel):
    a: str
    b: str


class FareRuleRequest(BaseModel):
    max_hops: int | None = None
    price: float
