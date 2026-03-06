# ─── Pydantic Schema ───
from pydantic import BaseModel
from typing import Optional


class ExtractedItem(BaseModel):
    product: str
    brand: Optional[str] = "Generic"
    quantity: float = 0
    category: Optional[str] = "misc"