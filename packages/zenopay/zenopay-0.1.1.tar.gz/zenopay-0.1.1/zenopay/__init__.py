"""ZenoPay."""

import json
import logging
import re
from dataclasses import asdict, dataclass, field
from typing import Optional, Union

import phonenumbers
import requests
from phonenumbers import PhoneNumber, geocoder

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

url_pattern = r"^(https?://[^\s/$.?#].[^\s]*)$"
email_pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
phone_pattern = r"^(\+?25[5|4])?\d{9,10}$"


@dataclass
class CheckoutSchema:
    """Base Checkout Structure."""

    buyer_name: str
    buyer_phone: str
    buyer_email: str
    amount: float
    webhook_url: Optional[str] = None
    metadata: Optional[dict] = None
    _country: Optional[str] = field(
        default="TZ",
        init=False,
    )

    @property
    def country(self) -> str:
        return self._country

    @country.setter
    def country(self, value: str):
        self._country = value

    def __post_init__(self):
        """Validate fields after initialization."""
        if len(self.buyer_name) < 3:
            msg = "buyer_name must be at least 3 characters"
            raise ValueError(msg)

        if not re.match(phone_pattern, self.buyer_phone):
            msg = "Invalid phone number format"
            raise ValueError(msg)
        phone_number = self.validate_phone_number(self.buyer_phone)
        self.country = geocoder.country_name_for_number(phone_number, "en")
        self.buyer_phone = phonenumbers.format_number(
            phone_number,
            phonenumbers.PhoneNumberFormat.E164,
        ).removeprefix("+")

        if not re.match(email_pattern, self.buyer_email):
            msg = "Invalid email format"
            raise ValueError(msg)

        if self.amount < 10:
            msg = "amount must be at least 10"
            raise ValueError(msg)

        if self.webhook_url and not re.match(url_pattern, self.webhook_url):
            msg = "Invalid webhook URL format"
            raise ValueError(msg)

    @staticmethod
    def validate_phone_number(value: str) -> PhoneNumber:
        """Check phone number field."""
        try:
            phone_number = value if isinstance(value, str) else str(value)
            phone_number = phonenumbers.parse(value, "TZ")
            if not phonenumbers.is_valid_number(phone_number):
                msg = "Invalid phone number"
                raise ValueError(msg)
            return phone_number
        except phonenumbers.phonenumberutil.NumberParseException as error:
            msg = "Invalid phone number"
            raise ValueError(msg) from error

    def model_dump(self, *, exclude_none: bool = False) -> dict:
        """Convert the dataclass to a dictionary, similar to Pydantic's model_dump."""
        data = asdict(self)
        if exclude_none:
            return {k: v for k, v in data.items() if v is not None}
        return data


@dataclass
class CardPaymentSchema(CheckoutSchema):
    """Card Payment Data schema."""

    redirect_url: Optional[str] = field(default=None)
    cancel_url: Optional[str] = field(default=None)
    billing_country: str = field(default="TZ")

    def __post_init__(self):
        """Validate fields after initialization."""
        super().__post_init__()

        if self.redirect_url and not re.match(url_pattern, self.redirect_url):
            msg = "Invalid redirect URL format"
            raise ValueError(msg)

        if self.cancel_url and not re.match(url_pattern, self.cancel_url):
            msg = "Invalid cancel URL format"
            raise ValueError(msg)

        if len(self.billing_country) > 2:
            msg = "billing_country must be at most 2 characters"
            raise ValueError(msg)


class ZenoPay:
    """ZenoPay Client."""

    BASE_URL: str = "https://api.zeno.africa"
    TIMEOUT: int = 15  # in seconds

    def __init__(self, account_id: str) -> None:
        """Initialize.

        Args:
            account_id: str

        Returns:
            None

        Example:
        >>> from zenopay import ZenoPay
        >>> zenopay = ZenoPay(account_id="zpxxxx")

        """
        self.account_id = account_id
        self._api_key = None
        self._secret_key = None

    @property
    def api_key(self) -> Optional[str]:
        """Client API Key."""
        return self._api_key

    @api_key.setter
    def api_key(self, value: str) -> None:
        """Set API key."""
        if isinstance(value, str):
            self._api_key = value
        else:
            msg = f"Expected str type but received {type(value)}"
            raise TypeError(msg)

    @property
    def secret_key(self) -> Optional[str]:
        """Client API Key."""
        return self._secret_key

    @property
    def headers(self) -> dict:
        """Headers."""
        return {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/x-www-form-urlencoded",
        }

    @secret_key.setter
    def secret_key(self, value: str) -> None:
        """Set Secret Key."""
        if isinstance(value, str):
            self._secret_key = value
        else:
            msg = f"Expected str type but received {type(value)}"
            raise TypeError(msg)

    def _post(
        self,
        url: str,
        data: dict,
        *,
        is_json: bool = False,
    ) -> dict:
        """Handle post Request.

        Args:
            url: str
            data: dict
            is_json:bool= False, whether data is to be sent as JSON

        Returns:
            dict

        """
        # Remove None values
        data = {k: v for k, v in data.items() if v}
        try:
            with requests.Session() as session:
                response = (
                    session.post(
                        url=url,
                        headers={
                            "Content-Type": "application/json",
                            "Accept": "application/json",
                        },
                        json=data,
                        timeout=self.TIMEOUT,
                    )
                    if is_json
                    else session.post(
                        url=url,
                        headers={
                            "Content-Type": "application/x-www-form-urlencoded",
                            "Accept": "application/x-www-form-urlencoded",
                        },
                        data=data,
                        timeout=self.TIMEOUT,
                    )
                )
                response.raise_for_status()

                return response.json()
        except (requests.ConnectionError, requests.RequestException) as error:
            msg = f"Exception occured: {error}"
            logging.exception(msg)
            return {"success": False, "message": "Error handling the request."}

    def mobile_checkout(self, data: Union[dict, CheckoutSchema]) -> dict:
        """Initiate Mobile paymennt.

        Args:
            data: Union[dict, CheckoutSchema]

        Returns:
            Response: dict

        Example:
        >>> from zenopay import ZenoPay
        >>> zenopay = ZenoPay(account_id="zpxxxx")
        >>> zenopay.api_key= ""
        >>> zenopay.secret_key = ""
        >>> data={"buyer_name":"jovine me","buyer_phone":"071xxxxxxx","buyer_email":"jovinexxxxxx@gmail.com","amount":1000}
        >>> zenopay.mobile_checkout(data)
        >>> {'status': 'success', 'message': 'Wallet payment successful', 'order_id': '6777ad7e327xxx'}

        """
        if not all([self.api_key, self.secret_key]):
            msg = "You must have api key and secret key set."
            raise ValueError(msg)
        _data = data if isinstance(data, CheckoutSchema) else CheckoutSchema(**data)
        data = _data.model_dump(exclude_none=True)
        data.update(
            {
                "create_order": 1,
                "api_key": self.api_key,
                "secret_key": self.secret_key,
                "account_id": self.account_id,
            },
        )
        self.BASE_URL = (
            f"{self.BASE_URL}/KE" if _data.country.lower() == "kenya" else self.BASE_URL
        )
        return self._post(
            url=self.BASE_URL,
            data=data,
            is_json=False,
        )

    def card_checkout(self, data: Union[dict, CardPaymentSchema]) -> dict:
        """Initiate Card Payment.

        Args:
            data: Union[dict, CardPaymentSchema]

        Returns:
            response: dict

        Example:
        >>> from zenopay import ZenoPay
        >>> zenopay = ZenoPay(account_id="zpxxxx")
        >>> data={"buyer_name":"jovine me","buyer_phone":"071xxxxxxx","buyer_email":"jovinexxxxxx@gmail.com","amount":1000,"metadata":{"product_id": "12345","color": "blue","size": "L","custom_notes": "Please gift-wrap this item."}}
        >>> zenopay.card_checkout(data)
        >>> {'status': 'success', 'message': 'Order created successfully', 'order_id': 'xxxxx', 'payment_link': 'https://secure.payment.tz/link'}

        """
        if not all([self.api_key, self.secret_key]):
            msg = "You must have api key and secret key set."
            raise ValueError(msg)
        _data = CardPaymentSchema(**data) if isinstance(data, dict) else data
        url = self.BASE_URL + "/card"
        data = _data.model_dump(exclude_none=True)
        data.update(
            {
                "billing.country": _data.billing_country or _data.country,
                "account_id": self.account_id,
                "api_key": self.api_key,
                "secret_key": self.secret_key,
                "metadata": json.dumps(data["metadata"])
                if data.get("metadata")
                else None,
            },
        )
        return self._post(url=url, data=data, is_json=True)

    def check_order_status(self, order_id: str) -> dict:
        """Check Order Status.

        Args:
            order_id: str

        Returns:
            response: dict ->

        Example:
        >>> from zenopay import ZenoPay
        >>> zenopay = ZenoPay(account_id="zpxxxx")
        >>> status= zenopay.check_order_status(order_id="12121212")
        >>> {'status': 'success', 'order_id': 'order_id', 'message': 'Order fetch successful', 'amount': '1000.00', 'payment_status': 'PENDING'}

        """
        if not isinstance(order_id, str):
            msg = f"Expected str type but received {type(order_id)}"
            raise TypeError(msg)
        url = self.BASE_URL + "/order-status"
        data = {
            "check_status": 1,
            "order_id": order_id,
            "api_key": self.api_key,
            "secret_key": self.secret_key,
        }
        return self._post(url=url, data=data, is_json=False)
