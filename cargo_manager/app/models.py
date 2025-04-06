from pydantic import BaseModel
from typing import Optional
from datetime import date

class Item(BaseModel):
    id: str
    name: str
    width: int
    depth: int
    height: int
    mass: float
    priority: int
    expiry_date: Optional[date]
    usage_limit: int
    preferred_zone: str
    current_uses: int = 0

class Container(BaseModel):
    id: str
    zone: str
    width: int
    depth: int
    height: int
