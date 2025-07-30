from click_up.classes.merchant import MerchantApi
from click_up.classes.initializer import Initializer


class ClickUp:
    """
    CLICK Up client class
    """
    def __init__(
        self,
        service_id,
        merchant_id,
        merchant_user_id=None,
        secret_key=None
    ):
        """
        Initialize Click object

        Args:
            service_id (str): Service ID provided by CLICK
            merchant_id (str): Merchant ID provided by CLICK
            merchant_user_id (str, optional):
                Merchant User ID provided by CLICK. Defaults to None.
            secret_key (str, optional):
                Secret key for authentication. Defaults to None.
        """
        self.initializer = Initializer(service_id, merchant_id)
        self.merchant_api = MerchantApi(
            service_id=service_id,
            merchant_user_id=merchant_user_id,
            secret_key=secret_key
        )
