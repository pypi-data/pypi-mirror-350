from typing import Optional
from pydantic import BaseModel


class ClickShopApiResponse(BaseModel):
    error: int
    click_trans_id: int
    merchant_trans_id: str
    error_note: Optional[str] = None
    merchant_confirm_id: Optional[int] = None
