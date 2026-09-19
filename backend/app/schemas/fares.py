from pydantic import BaseModel


class FareRuleIn(BaseModel):
    max_hops: int | None = None
    price: float
