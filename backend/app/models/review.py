from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    poi_id = Column(Integer, ForeignKey("pois.id", ondelete="CASCADE"), nullable=False)
    user_name = Column(String(100), default="anonymous")
    rating = Column(Float, nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    poi = relationship("POI", back_populates="reviews")
