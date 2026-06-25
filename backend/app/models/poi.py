from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from ..database import Base

class POI(Base):
    __tablename__ = "pois"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    address = Column(String(300))
    phone = Column(String(30))
    description = Column(Text)
    rating = Column(Float, default=0)
    lng = Column(Float, nullable=False)
    lat = Column(Float, nullable=False)
    geom = Column(Geometry("POINT", 4326))
    
    category = relationship("Category", back_populates="pois")
    reviews = relationship("Review", back_populates="poi", cascade="all, delete-orphan")
