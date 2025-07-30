from pydantic import BaseModel

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from clickup_fastapi.models.transaction import Base


class ClickSettings(BaseModel):
    service_id: str
    secret_key: str
    merchant_id: str
    commission_percent: float = 0.0


def click_database_manager(db_url: str):
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    return SessionLocal
