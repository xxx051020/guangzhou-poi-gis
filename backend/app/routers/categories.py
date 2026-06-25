from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..database import get_db
from ..models.category import Category
from ..schemas.category import CategoryCreate, CategoryResponse

router = APIRouter(prefix="/api/categories", tags=["Categories"])

@router.get("", response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    return db.execute(select(Category)).scalars().all()

@router.post("", response_model=CategoryResponse, status_code=201)
def create_category(data: CategoryCreate, db: Session = Depends(get_db)):
    c = Category(**data.model_dump())
    db.add(c)
    db.commit()
    db.refresh(c)
    return c
