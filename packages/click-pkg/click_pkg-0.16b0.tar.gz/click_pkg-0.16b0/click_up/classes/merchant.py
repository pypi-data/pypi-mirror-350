import time
import hashlib

from click_up.classes.http import Http


class MerchantApi:
    """
    A class for interacting with the CLICK Merchant API.
    """

    def __init__(self, service_id, merchant_user_id, secret_key):
        """
        Initialize the MerchantApi instance.

        Args:
            url (str): Base URL of the CLICK Merchant API.
            merchant_user_id (str): Merchant User ID provided by CLICK.
            secret_key (str): Secret key for authentication.
        """
        self.http = Http()
        self.secret_key = secret_key
        self.service_id = service_id
        self.merchant_user_id = merchant_user_id
        self.url = "https://api.click.uz/v2/merchant"

    def create_invoice(
        self,
        amount,
        phone_number,
        merchant_trans_id
    ):
        """
        Create an invoice using the CLICK API.

        Args:
            service_id (int): Service ID.
            amount (float): Requested amount.
            phone_number (str): Invoice receiver.
            merchant_trans_id (str):
                Order ID (for online shopping) / personal account / login
                in the billing of the supplier.
        Returns:
            dict: A dictionary containing the response from the API.
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
        return self.http.post(url, body, headers, 10)
