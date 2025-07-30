# click_fastapi/core/merchant.py
import time
import hashlib
from .http import Http


class MerchantApi:
    def __init__(
        self, service_id: str, secret_key: str, merchant_user_id: str = None
    ):
        self.http = Http()
        self.secret_key = secret_key
        self.service_id = service_id
        self.merchant_user_id = merchant_user_id
        self.url = "https://api.click.uz/v2/merchant"

    async def create_invoice(
        self,
        amount: float,
        phone_number: str,
        merchant_trans_id: str
    ):
        """
        CLICK API orqali hisob yaratish (asinxron).
        """
        timestamp = int(time.time())
        digest_input = f"{timestamp}{self.secret_key}"
        digest = hashlib.sha1(digest_input.encode()).hexdigest()
        headers = {
            "Auth": f"{self.merchant_user_id}:{digest}:{timestamp}",
        }
        body = {
            "service_id": self.service_id,
            "amount": amount,
            "phone_number": phone_number,
            "merchant_trans_id": merchant_trans_id
        }
        url = f"{self.url}/invoice/create"
        return await self.http.post(url, body, headers, 10)
