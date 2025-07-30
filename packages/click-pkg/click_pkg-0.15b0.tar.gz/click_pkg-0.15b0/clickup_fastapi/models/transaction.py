from datetime import datetime

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime


Base = declarative_base()


class ClickTransaction(Base):
    __tablename__ = "click_transactions"

    id = Column(Integer, primary_key=True, index=True)
    state = Column(Integer, default=0)
    transaction_id = Column(String(255), nullable=False)
    account_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    CREATED = 0
    INITIATING = 1
    SUCCESSFULLY = 2
    CANCELLED = -2
