from typing import Optional
from pydantic import BaseModel

from clickup_fastapi.utils.const import Action
from clickup_fastapi.utils import exceptions


class ClickShopApiRequest(BaseModel):
    click_trans_id: str
    service_id: str
    click_paydoc_id: str
    merchant_trans_id: str
    amount: str
    action: str
    error: str
    sign_time: str
    sign_string: str
    error_note: Optional[str] = None
    merchant_prepare_id: Optional[int] = None

    def is_valid(self):
        self.check_fields()
        self.check_allowed_action()

    def check_allowed_action(self):
        if self.action not in Action.ALLOWED_ACTIONS:
            raise exceptions.UnSupportedAction("unsupported invalid action")

    def check_fields(self):
        if self.action == Action.PREPARE and self.merchant_trans_id is None:
            raise exceptions.BadRequest(
                "missing required field 'merchant_trans_id'"
            )
