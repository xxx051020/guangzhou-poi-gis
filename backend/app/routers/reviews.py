from fastapi import APIRouter, Depends
from ..database import get_db

router = APIRouter(prefix="/api/reviews", tags=["Reviews"])
