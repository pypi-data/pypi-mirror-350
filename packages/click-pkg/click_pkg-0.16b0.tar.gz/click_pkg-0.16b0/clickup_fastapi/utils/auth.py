
import hashlib

from clickup_fastapi.schemas.request import ClickShopApiRequest
from clickup_fastapi.utils.exceptions import AuthFailed


def check_auth(params: ClickShopApiRequest, service_id: str, secret_key: str):
    if not all([service_id, secret_key]):
        raise AuthFailed("Missing required settings: service_id or secret_key")

    text_parts = [
        params.click_trans_id, service_id,
        secret_key, params.merchant_trans_id,
        str(params.merchant_prepare_id or ""),
        params.amount, params.action, params.sign_time
    ]
    calculated_hash = \
        hashlib.md5(''.join(text_parts).encode('utf-8')).hexdigest()

    if calculated_hash != params.sign_string:
        raise AuthFailed("invalid signature")
