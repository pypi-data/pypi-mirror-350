import logging

from sqlalchemy.orm import Session

from clickup_fastapi.utils import exceptions
from clickup_fastapi.utils.const import Action
from clickup_fastapi.utils.auth import check_auth
from clickup_fastapi.dependencies import ClickSettings
from clickup_fastapi.schemas.request import ClickShopApiRequest
from clickup_fastapi.models.transaction import ClickTransaction


logger = logging.getLogger(__name__)


class Account:
    def __init__(self, id: int, amount: float):
        self.id = id
        self.amount = amount


def _validate_amount(received_amount: float, expected_amount: float):
    if abs(received_amount - expected_amount) > 0.01:
        raise exceptions.IncorrectAmount("Incorrect parameter amount")


def _check_transaction_state(db: Session, merchant_trans_id: str):
    if db.query(ClickTransaction).filter(
        ClickTransaction.account_id == merchant_trans_id,
        ClickTransaction.state == ClickTransaction.SUCCESSFULLY
    ).first():
        raise exceptions.AlreadyPaid("Transaction already paid")
    if db.query(ClickTransaction).filter(
        ClickTransaction.account_id == merchant_trans_id,
        ClickTransaction.state == ClickTransaction.CANCELLED
    ).first():
        raise exceptions.TransactionCancelled("Transaction cancelled")


def _get_or_create_transaction(
    db: Session,
    account_id: int,
    amount: float,
    click_trans_id: str,
    state: int
):
    transaction = db.query(ClickTransaction).filter(
        ClickTransaction.transaction_id == click_trans_id
    ).first()
    if not transaction:
        transaction = ClickTransaction(
            account_id=account_id,
            amount=amount,
            transaction_id=click_trans_id,
            state=state
        )
        db.add(transaction)
    else:
        transaction.state = state
    db.commit()
    db.refresh(transaction)
    return transaction


async def process_webhook(
    params: ClickShopApiRequest,
    db: Session,
    settings: ClickSettings,
    account: Account = None
):
    params = ClickShopApiRequest(
        click_trans_id=params.get("click_trans_id"),
        service_id=params.get("service_id"),
        click_paydoc_id=params.get("click_paydoc_id"),
        merchant_trans_id=params.get("merchant_trans_id"),
        amount=params.get("amount"),
        action=params.get("action"),
        error=params.get("error"),
        sign_time=params.get("sign_time"),
        sign_string=params.get("sign_string"),
        error_note=params.get("error_note"),
        merchant_prepare_id=params.get("merchant_prepare_id")
    )

    logger.info(f"Incoming params: {params}")

    check_auth(params, settings.service_id, settings.secret_key)
    params.is_valid()

    received_amount = float(params.amount)
    commission = settings.commission_percent / 100
    expected_amount = round(account.amount * (1 + commission), 2)
    _validate_amount(received_amount, expected_amount)

    _check_transaction_state(db, params.merchant_trans_id)

    if int(params.error) < 0:
        raise exceptions.TransactionCancelled("Transaction cancelled")

    if params.action == Action.PREPARE:
        transaction = _get_or_create_transaction(
            db, account.id, float(params.amount),
            params.click_trans_id, ClickTransaction.INITIATING
        )
        error_note = "success"

    elif params.action == Action.COMPLETE:
        is_successful = int(params.error) >= 0
        state = ClickTransaction.SUCCESSFULLY if is_successful else ClickTransaction.CANCELLED # noqa
        transaction = _get_or_create_transaction(
            db, account.id, float(params.amount),
            params.click_trans_id, state
        )
        error_note = params.error_note
        status = 'successful' if state == ClickTransaction.SUCCESSFULLY else 'cancelled' # noqa
        logger.info(f"Payment {status}: {params}")

    else:
        raise exceptions.UnSupportedAction("Unknown action")

    return {
        "click_trans_id": params.click_trans_id,
        "merchant_trans_id": str(account.id),
        "merchant_prepare_id": transaction.id,
        "error": int(params.error),
        "error_note": error_note
    }
