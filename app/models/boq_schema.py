# ─── Pydantic Schema ───
from pydantic import BaseModel, Field
from typing import Optional, List


# This is the rule for a single item
class BOQItem(BaseModel):
    description: str = Field(description="The name/description of the material or work item")
    brand: Optional[str] = Field(description="The manufacturer or brand if mentioned", default="Generic")
    quantity: Optional[float] = Field(description="The number/amount. Use 0 if not clearly stated.", default=0.0)
    unit: Optional[str] = Field(description="How it is measured (kg, m, nos, sets, etc). Use '-' if unknown.", default="-")
    category: Optional[str] = Field(description="EPC industry category (Electrical, Plumbing, Civil, etc)", default="Uncategorized")

# This is the rule for the whole list
class BOQList(BaseModel):
    items: List[BOQItem]