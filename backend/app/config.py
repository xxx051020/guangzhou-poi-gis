from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_ENV: str = "development"
    DATABASE_URL: str = "postgresql://gis_user:gis_pass_2024@localhost:5432/gz_poi_db"
    
    class Config:
        env_file = ".env"

settings = Settings()
