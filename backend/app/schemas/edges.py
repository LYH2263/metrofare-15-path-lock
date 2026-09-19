from pydantic import BaseModel


class EdgeIn(BaseModel):
    a: str
    b: str
