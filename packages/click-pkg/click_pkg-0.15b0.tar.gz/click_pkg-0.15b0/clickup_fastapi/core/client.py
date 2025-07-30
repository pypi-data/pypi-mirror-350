from .merchant import MerchantApi
from .initializer import Initializer


class ClickUp:
    def __init__(
        self,
        service_id: str,
        merchant_id: str,
        secret_key: str = None
    ):
        self.initializer = Initializer(service_id, merchant_id)
        self.merchant_api = MerchantApi(
            service_id=service_id,
            secret_key=secret_key
        )
