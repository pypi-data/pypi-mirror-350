import logging

from fastapi import HTTPException


logger = logging.getLogger(__name__)


class BaseClickException(HTTPException):
    def __init__(self, error_code: int, message: str = None):
        detail = {"error": {"error": error_code, "error_note": message}}
        logger.error(f"click error detail: {detail}")
        super().__init__(status_code=200, detail=detail)


class UnSupportedAction(BaseClickException):
    def __init__(self, message: str = "unsupported invalid action"):
        super().__init__(error_code=-3, message=message)


class BadRequest(BaseClickException):
    def __init__(self, message: str = "bad request"):
        super().__init__(error_code=-8, message=message)


class AuthFailed(BaseClickException):
    def __init__(self, message: str = "authentication failed"):
        super().__init__(error_code=-1, message=message)


class AccountNotFound(BaseClickException):
    def __init__(self, message: str = "account not found"):
        super().__init__(error_code=-1, message=message)


class IncorrectAmount(BaseClickException):
    def __init__(self, message: str = "incorrect amount"):
        super().__init__(error_code=-2, message=message)


class AlreadyPaid(BaseClickException):
    def __init__(self, message: str = "transaction already paid"):
        super().__init__(error_code=-4, message=message)


class TransactionNotFound(BaseClickException):
    def __init__(self, message: str = "transaction not found"):
        super().__init__(error_code=-6, message=message)


class TransactionCancelled(BaseClickException):
    def __init__(self, message: str = "transaction cancelled"):
        super().__init__(error_code=-9, message=message)


errors_whitelist = (
    UnSupportedAction, BadRequest, AuthFailed, AccountNotFound,
    IncorrectAmount, AlreadyPaid, TransactionNotFound, TransactionCancelled
)
