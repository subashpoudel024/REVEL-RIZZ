from pydantic import BaseModel

class PickupFormatter(BaseModel):
    pickup_line1: str
    pickup_line2: str
    pickup_line3: str
    pickup_line4: str