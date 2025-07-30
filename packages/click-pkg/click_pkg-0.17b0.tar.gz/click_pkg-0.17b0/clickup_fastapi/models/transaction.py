from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime

from clickup_fastapi.utils.timezone import utc_now


Base = declarative_base()


class ClickTransaction(Base):
    """
    SQLAlchemy model for Click payment transactions.

    This model stores transaction data for Click payment processing,
    including transaction state, amounts, and timestamps.
    """
    __tablename__ = "click_transactions"

    id = Column(Integer, primary_key=True, index=True)
    state = Column(Integer, default=0)
    transaction_id = Column(String(255), nullable=False)
    account_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(
        DateTime, default=utc_now, onupdate=utc_now
    )

    CREATED = 0
    INITIATING = 1
    SUCCESSFULLY = 2
    CANCELLED = -2
