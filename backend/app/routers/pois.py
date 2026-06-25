from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, func, text
from geoalchemy2.shape import to_shape
from geoalchemy2.functions import ST_DWithin, ST_MakeEnvelope, ST_AsGeoJSON
from geojson import Feature, FeatureCollection, Point as GeoPoint
from typing import Optional
import json

from ..database import get_db
from ..models.poi import POI
from ..models.review import Review
from ..schemas.poi import POICreate, POIResponse, POIUpdate
from ..schemas.review import ReviewCreate, ReviewResponse
from ..services.geo_service import haversine_distance, bbox_from_center

router = APIRouter(prefix="/api/pois", tags=["POIs"])

def poi_to_dict(p):
    return {"id": p.id, "name": p.name, "category_id": p.category_id,
            "address": p.address, "phone": p.phone, "description": p.description,
            "rating": p.rating, "lng": p.lng, "lat": p.lat}

# 1. List all POIs
@router.get("", response_model=list[POIResponse])
def list_pois(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.execute(select(POI).offset(skip).limit(limit)).scalars().all()

# 2. Get POI by ID
@router.get("/{poi_id}", response_model=POIResponse)
def get_poi(poi_id: int, db: Session = Depends(get_db)):
    poi = db.get(POI, poi_id)
    if not poi:
        raise HTTPException(status_code=404, detail="POI not found")
    return poi

# 3. Create POI
@router.post("", response_model=POIResponse, status_code=201)
def create_poi(data: POICreate, db: Session = Depends(get_db)):
    poi = POI(**data.model_dump(), geom=f"SRID=4326;POINT({data.lng} {data.lat})")
    db.add(poi)
    db.commit()
    db.refresh(poi)
    return poi

# 4. Update POI
@router.put("/{poi_id}", response_model=POIResponse)
def update_poi(poi_id: int, data: POIUpdate, db: Session = Depends(get_db)):
    poi = db.get(POI, poi_id)
    if not poi:
        raise HTTPException(status_code=404, detail="POI not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(poi, k, v)
    if data.lng is not None and data.lat is not None:
        poi.geom = f"SRID=4326;POINT({data.lng} {data.lat})"
    db.commit()
    db.refresh(poi)
    return poi

# 5. Delete POI
@router.delete("/{poi_id}")
def delete_poi(poi_id: int, db: Session = Depends(get_db)):
    poi = db.get(POI, poi_id)
    if not poi:
        raise HTTPException(status_code=404, detail="POI not found")
    db.delete(poi)
    db.commit()
    return {"detail": "deleted"}

# 6. Filter by category
@router.get("/filter/category/{category_id}")
def filter_by_category(category_id: int, db: Session = Depends(get_db)):
    rows = db.execute(select(POI).where(POI.category_id == category_id)).scalars().all()
    return [poi_to_dict(r) for r in rows]

# 7. Search by keyword
@router.get("/search/")
def search_pois(keyword: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    rows = db.execute(
        select(POI).where(
            POI.name.ilike(f"%{keyword}%") | POI.description.ilike(f"%{keyword}%")
        ).limit(50)
    ).scalars().all()
    return {"keyword": keyword, "count": len(rows), "results": [poi_to_dict(r) for r in rows]}

# 8. Nearby search
@router.get("/nearby/")
def nearby_pois(lng: float, lat: float, radius: float = 3000, db: Session = Depends(get_db)):
    point = f"SRID=4326;POINT({lng} {lat})"
    rows = db.execute(
        select(POI, ST_DWithin(POI.geom, point, radius).label("within"))
        .where(ST_DWithin(POI.geom, point, radius))
    ).all()
    results = []
    for row, _ in rows:
        d = poi_to_dict(row)
        d["distance_m"] = round(haversine_distance(lat, lng, row.lat, row.lng), 1)
        results.append(d)
    results.sort(key=lambda x: x["distance_m"])
    return {"center": {"lng": lng, "lat": lat}, "radius": radius, "count": len(results), "results": results}

# 9. Rectangle/bbox search
@router.get("/bbox/")
def bbox_search(west: float, south: float, east: float, north: float, db: Session = Depends(get_db)):
    env = ST_MakeEnvelope(west, south, east, north, 4326)
    rows = db.execute(
        select(POI).where(func.ST_Intersects(POI.geom, env))
    ).scalars().all()
    return {"bbox": {"west": west, "south": south, "east": east, "north": north}, "count": len(rows), "results": [poi_to_dict(r) for r in rows]}

# 10. All POIs as GeoJSON
@router.get("/geojson/all")
def pois_geojson(db: Session = Depends(get_db)):
    pois = db.execute(select(POI)).scalars().all()
    features = []
    for p in pois:
        features.append(Feature(geometry=GeoPoint((p.lng, p.lat)), properties=poi_to_dict(p)))
    return FeatureCollection(features)

# 11. Single POI as GeoJSON
@router.get("/geojson/{poi_id}")
def poi_geojson(poi_id: int, db: Session = Depends(get_db)):
    poi = db.get(POI, poi_id)
    if not poi:
        raise HTTPException(status_code=404, detail="POI not found")
    return Feature(geometry=GeoPoint((poi.lng, poi.lat)), properties=poi_to_dict(poi))

# 12. Statistics
@router.get("/stats/")
def poi_stats(db: Session = Depends(get_db)):
    total = db.execute(select(func.count(POI.id))).scalar()
    cats = db.execute(select(POI.category_id, func.count(POI.id)).group_by(POI.category_id)).all()
    avg_rating = db.execute(select(func.avg(POI.rating))).scalar()
    return {"total": total, "by_category": [{"category_id": c[0], "count": c[1]} for c in cats], "avg_rating": round(float(avg_rating or 0), 2)}

# 13. POI reviews
@router.get("/{poi_id}/reviews", response_model=list[ReviewResponse])
def get_reviews(poi_id: int, db: Session = Depends(get_db)):
    return db.execute(select(Review).where(Review.poi_id == poi_id)).scalars().all()

# 14. Add review
@router.post("/reviews", response_model=ReviewResponse, status_code=201)
def add_review(data: ReviewCreate, db: Session = Depends(get_db)):
    if not db.get(POI, data.poi_id):
        raise HTTPException(status_code=404, detail="POI not found")
    r = Review(**data.model_dump())
    db.add(r)
    db.commit()
    db.refresh(r)
    return r
