from pydantic import BaseModel, condecimal
from datetime import datetime

class OrderCreate(BaseModel):
    total_amount: condecimal(gt=0)

class OrderResponse(BaseModel):
    id: int
    user_id: int
    order_date: datetime
    total_amount: float
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
