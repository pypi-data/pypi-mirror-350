"""
CLICK payment system webhook views.

This module contains the main webhook handler for processing CLICK payment
transactions, including fiscal item validation and processing.
"""
import logging
import hashlib
from typing import List, Dict, Any, Optional

from django.conf import settings
from django.utils.module_loading import import_string

from rest_framework.views import APIView
from rest_framework.response import Response

from click_up import exceptions
from click_up.const import Action
from click_up.models import ClickTransaction
from click_up.typing.request import ClickShopApiRequest

logger = logging.getLogger(__name__)
AccountModel = import_string(settings.CLICK_ACCOUNT_MODEL)


# pylint: disable=W1203,E1101,W0707


class ClickWebhook(APIView):
    """
    API endpoint for handling incoming CLICK webhooks.
    """
    def post(self, request):
        """
        Check if request is valid
        """
        # check 1 validation
        result = None
        params: ClickShopApiRequest = self.serialize(request)
        account = self.fetch_account(params)

        # check 2 check perform transaction
        self.check_perform_transaction(account, params)

        if params.action == Action.PREPARE:
            result = self.create_transaction(account, params)

        elif params.action == Action.COMPLETE:
            result = self.perform_transaction(account, params)

        return Response(result)

    def serialize(self, request):
        """
        serialize request data to object
        """
        request_data = {
            'click_trans_id': request.POST.get('click_trans_id'),
            'service_id': request.POST.get('service_id'),
            'click_paydoc_id': request.POST.get('click_paydoc_id'),
            'merchant_trans_id': request.POST.get('merchant_trans_id'),
            'amount': request.POST.get('amount'),
            'action': request.POST.get('action'),
            'error': request.POST.get('error'),
            'sign_time': request.POST.get('sign_time'),
            'sign_string': request.POST.get('sign_string'),
            'error_note': request.POST.get('error_note'),
            'merchant_prepare_id': request.POST.get('merchant_prepare_id'),
        }

        try:
            request_data = ClickShopApiRequest(**request_data)
            self.check_auth(request_data)

            request_data.is_valid()
            return request_data

        except exceptions.errors_whitelist as exc:
            raise exc

        except Exception as exc:
            logger.error(f"error in request data: {exc}")
            raise exceptions.BadRequest("error in request from click")

    def check_auth(self, params, service_id=None, secret_key=None):
        """
        Verifies the authenticity of the transaction using the secret key.

        :return: True if the signature is valid,
            otherwise raises an AuthFailed exception.
        """
        # by default it should be get from settings
        # in the another case u can override
        if not secret_key or not service_id:
            service_id = settings.CLICK_SERVICE_ID
            secret_key = settings.CLICK_SECRET_KEY

        if not all([service_id, secret_key]):
            error = "Missing required CLICK_SETTINGS: service_id, secret_key, or merchant_id" # noqa
            raise exceptions.AuthFailed(error)

        text_parts = [
            params.click_trans_id,
            service_id,
            secret_key,
            params.merchant_trans_id,
            params.merchant_prepare_id or "",
            params.amount,
            params.action,
            params.sign_time,
        ]
        text = ''.join(map(str, text_parts))

        calculated_hash = hashlib.md5(text.encode('utf-8')).hexdigest()

        if calculated_hash != params.sign_string:
            raise exceptions.AuthFailed("invalid signature")

    def fetch_account(self, params: ClickShopApiRequest):
        """
        fetching account for given merchant transaction id
        """
        try:
            return AccountModel.objects.get(id=params.merchant_trans_id)

        except AccountModel.DoesNotExist:
            raise exceptions.AccountNotFound("Account not found")

    def check_amount(self, account: AccountModel, params: ClickShopApiRequest):  # type: ignore  # noqa
        """
        Validate the received amount, considering optional commission percent.
        """
        received_amount = float(params.amount)
        base_amount = float(getattr(account, settings.CLICK_AMOUNT_FIELD))
        commission_percent = getattr(settings, "CLICK_COMMISSION_PERCENT", 0)

        expected_amount = round(base_amount * (1 + commission_percent / 100), 2) # noqa

        if abs(received_amount - expected_amount) > 0.01:
            raise exceptions.IncorrectAmount("Incorrect parameter amount")

    def check_dublicate_transaction(self, params: ClickShopApiRequest):  # type: ignore # noqa
        """
        check if transaction already exist
        """
        if ClickTransaction.objects.filter(
            account_id=params.merchant_trans_id,
            state=ClickTransaction.SUCCESSFULLY
        ).exists():
            raise exceptions.AlreadyPaid("Transaction already paid")

    def check_transaction_cancelled(self, params: ClickShopApiRequest):
        """
        check if transaction cancelled
        """
        if ClickTransaction.objects.filter(
            account_id=params.merchant_trans_id,
            state=ClickTransaction.CANCELLED
        ).exists() or int(params.error) < 0:
            raise exceptions.TransactionCancelled("Transaction cancelled")

    def check_perform_transaction(self, account: AccountModel, params: ClickShopApiRequest): # type: ignore # noqa
        """
        Check perform transaction with CLICK system
        """
        self.check_amount(account, params)
        self.check_dublicate_transaction(params)
        self.check_transaction_cancelled(params)

    def add_fiscal_items(
        self,
        items: Optional[List[Dict[str, Any]]] = None
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Adds and validates fiscal items for the transaction.

        This method processes, validates, and attaches fiscal items to the
        transaction payload. It performs comprehensive validation of fiscal
        data including VAT calculations, required fields, and data types.
        Note: This method does NOT validate total amounts against account.

        Parameters:
            items (list, optional): List of fiscal item dictionaries.
                Each item must contain:
                - Name (str): Product name (max 255 chars)
                - SPIC (str): Standard Product Identification Code (17 digits)
                - PackageCode (str): Unique product packaging code
                - Price (int): Unit price in smallest currency unit
                - Amount (int): Quantity (positive integer)
                - VAT (int): VAT amount in smallest currency unit
                - VATPercent (int): VAT percentage (0-100)
                - CommissionInfo (dict, optional): Commission details
                    - TIN (str): Tax Identification Number

        Returns:
            list: Validated fiscal items or None if no items provided

        Raises:
            BadRequest: If fiscal items are invalid or malformed

        Example:
            items = [
                {
                    "Name": "Product Name",
                    "SPIC": "02104002001000000",
                    "PackageCode": "1476286",
                    "Price": 100000,
                    "Amount": 1000,
                    "VAT": 10714,
                    "VATPercent": 12,
                    "CommissionInfo": {"TIN": "311776491"}
                }
            ]
        """
        if not items:
            logger.debug("No fiscal items provided")
            return items

        try:
            logger.info(f"Processing {len(items)} fiscal items")
            validated_items = []

            for index, item in enumerate(items):
                validated_item = self._validate_fiscal_item(item, index)
                validated_items.append(validated_item)

            logger.info(
                f"Successfully validated {len(validated_items)} fiscal items"
            )
            return validated_items

        except exceptions.BadRequest as exc:
            raise exc

        except Exception as exc:
            logger.error(f"Error processing fiscal items: {exc}")
            raise exceptions.BadRequest(
                f"Invalid fiscal items format: {str(exc)}"
            )

    def _validate_fiscal_item(
        self, item: Dict[str, Any], index: int
    ) -> Dict[str, Any]:
        """
        Validates a single fiscal item.

        Args:
            item: Fiscal item dictionary to validate
            index: Item index for error reporting

        Returns:
            Validated fiscal item dictionary

        Raises:
            BadRequest: If item validation fails
        """
        if not isinstance(item, dict):
            raise exceptions.BadRequest(
                f"Fiscal item {index} must be a dictionary"
            )

        required_fields = [
            'Name', 'SPIC', 'PackageCode', 'Price', 'Amount', 'VAT',
            'VATPercent'
        ]

        for field in required_fields:
            if field not in item:
                raise exceptions.BadRequest(
                    f"Missing required field '{field}' in fiscal item {index}"
                )

        validated_item = {}

        name = item['Name']
        if not isinstance(name, str) or not name.strip():
            raise exceptions.BadRequest(
                f"Name must be a non-empty string in item {index}"
            )

        if len(name) > 255:
            raise exceptions.BadRequest(
                f"Name too long (max 255 chars) in item {index}"
            )

        validated_item['Name'] = name.strip()

        spic = str(item['SPIC'])
        if not spic.isdigit():
            raise exceptions.BadRequest(
                f"SPIC must be digits in item {index}"
            )

        validated_item['SPIC'] = spic

        package_code = str(item['PackageCode'])
        if not package_code.strip():
            raise exceptions.BadRequest(
                f"PackageCode cannot be empty in item {index}"
            )
        validated_item['PackageCode'] = package_code.strip()

        for field in ['Price', 'Amount', 'VAT']:
            value = item[field]
            if not isinstance(value, (int, float)) or value < 0:
                raise exceptions.BadRequest(
                    f"{field} must be a non-negative number in item {index}"
                )
            validated_item[field] = int(value)

        vat_percent = item['VATPercent']
        if not isinstance(vat_percent, (int, float)) or 0 > vat_percent > 100:
            raise exceptions.BadRequest(
                f"VATPercent must be between 0-100 in item {index}"
            )
        validated_item['VATPercent'] = int(vat_percent)

        if 'CommissionInfo' in item:
            commission_info = item['CommissionInfo']
            if isinstance(commission_info, dict) and 'TIN' in commission_info:
                tin = str(commission_info['TIN'])
                if tin.strip():
                    validated_item['CommissionInfo'] = {'TIN': tin.strip()}

        return validated_item

    def create_transaction(self, account: AccountModel, params: ClickShopApiRequest): # type: ignore # noqa
        """
        Create transaction in your system with fiscal items validation.
        """
        transaction = ClickTransaction.get_or_create(
            account_id=account.id,
            amount=params.amount,
            transaction_id=params.click_trans_id
        )
        fiscal_items = self.get_fiscal_items_for_account(account)

        validated_fiscal_items = self.add_fiscal_items(
            items=fiscal_items
        )

        # callback event
        self.created_payment(params)
        response = {
            "click_trans_id": params.click_trans_id,
            "merchant_trans_id": account.id,
            "merchant_prepare_id": transaction.id,
            "error": 0,
            "error_note": "success"
        }
        if validated_fiscal_items:
            response['fiscal_items'] = validated_fiscal_items

        return response

    def get_fiscal_items_for_account(
        self, account: Any
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get fiscal items for the given account.

        This method can be overridden to provide custom fiscal items
        based on the account or transaction data.

        Args:
            account: The account model instance

        Returns:
            List of fiscal items or None if not applicable
        """
        if hasattr(account, 'get_fiscal_items'):
            return account.get_fiscal_items()

        return None

    def perform_transaction(self, account: AccountModel, params: ClickShopApiRequest): # type: ignore # noqa
        """
        perform transaction with CLICK system
        """
        state = ClickTransaction.SUCCESSFULLY

        if params.error is not None:
            if int(params.error) < 0:
                state = ClickTransaction.CANCELLED

        transaction = ClickTransaction.update_or_create(
            account_id=account.id,
            amount=params.amount,
            transaction_id=params.click_trans_id,
            state=state
        )

        # callback event
        if state == ClickTransaction.SUCCESSFULLY:
            self.successfully_payment(params)

        elif state == ClickTransaction.CANCELLED:
            self.cancelled_payment(params)

        return {
            "click_trans_id": params.click_trans_id,
            "merchant_trans_id": transaction.account_id,
            "merchant_prepare_id": transaction.id,
            "error": params.error,
            "error_note": params.error_note
        }

    def created_payment(self, params):
        """
        created payment method process you can ovveride it
        """

    def successfully_payment(self, params):
        """
        successfully payment method process you can ovveride it
        """
        print(f"payment successful params: {params}")

    def cancelled_payment(self, params):
        """
        cancelled payment method process you can ovveride it
        """
        print(f"payment cancelled params: {params}")
