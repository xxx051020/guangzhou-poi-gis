from pydantic import BaseModel
from typing import Optional

class POIBase(BaseModel):
    name: str
    category_id: int
    address: Optional[str] = None
    phone: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[float] = 0
    lng: float
    lat: float

class POICreate(POIBase):
    pass

class POIResponse(POIBase):
    id: int
    class Config:
        from_attributes = True

class POIUpdate(BaseModel):
    name: Optional[str] = None
    category_id: Optional[int] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[float] = None
    lng: Optional[float] = None
    lat: Optional[float] = None
