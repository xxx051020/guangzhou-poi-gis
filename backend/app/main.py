import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import pois, categories, reviews

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="?? POI ??????",
    description="?? FastAPI + PostGIS + OpenLayers ??????????????",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pois.router)
app.include_router(categories.router)
app.include_router(reviews.router)

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "?? POI ??????"}
