

class Initializer:
    def __init__(self, service_id: str, merchant_id: str):
        self.service_id = service_id
        self.merchant_id = merchant_id

    async def generate_pay_link(self, id: str, amount: float, return_url: str):
        base_url = "https://my.click.uz/services/pay"
        paylik_url = (
            f"{base_url}?service_id={self.service_id}"
            f"&merchant_id={self.merchant_id}"
            f"&amount={amount}&transaction_param={id}"
            f"&return_url={return_url}"
        )
        return paylik_url
