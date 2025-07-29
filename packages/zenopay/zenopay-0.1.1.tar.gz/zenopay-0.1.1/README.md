# zenopay

Python Wrapper to Zenopay Payment. This wrapper is a simple way to interact with Zenopay Payment API.

You can get you account and API key from [Zenopay](https://zenopay.net/). You will need to have an account to access the API.

## Installation

```bash
pip install zenopay
```

## Usage

This assumes that you keep your credentials in a `.env` file. You can also set the environment variables directly. Let create an instance of the Zenopay class that will be used to interact with the API [It will  be reused in the examples below].

```python
import os
from dotenv import load_dotenv
from zenopay import ZenoPay

load_dotenv()

zenopay_client=ZenoPay(account_id=os.getenv('ZENOPAY_ACCOUNT_ID'))
```

NOTE: Webhook url set should be the endpoint that receives a POST request from Zenopay after a transaction is completed.

### Mobile Checkout

To initiate a mobile checkout, you will need to set client's api_key and sceret_key. You can get these from your Zenopay account.

Currently, supports only support Tanzania and Kenya.

```python
zenopay_client.api_key=os.getenv('ZENOPAY_API_KEY')
zenopay_client.secret_key=os.getenv('ZENOPAY_SECRET_KEY')

# Data to be sent to Zenopay
data = {
    "buyer_name": "jovine me",
    "buyer_phone": "0718193343", # Suggested phone number to have country code
    "buyer_email": "jovinerobotics@gmail.com",
    "amount": 1000,
    "webhook_url": "https://jovine.me/zenopay/webhook",
    "metadata":{
        "product_id": "12345",
        "color": "blue",
        "size": "L",
        "custom_notes": "Please gift-wrap this item."
    },
}

# Initiate a mobile checkout
checkout=zenopay_client.mobile_checkout(data)

# Print the response
print(checkout)
# {'status': 'success', 'message': 'Wallet payment successful', 'order_id': '6777ad7e327xxx'}
```

### Card Checkout

To initiate a card checkout, you will need to set client's api_key and sceret_key. You can get these from your Zenopay account.

```python
zenopay_client.api_key=os.getenv('ZENOPAY_API_KEY')
zenopay_client.secret_key=os.getenv('ZENOPAY_SECRET_KEY')

# Data to be sent to Zenopay

data = {
    "buyer_name": "jovine me",
    "buyer_phone": "0718193343",
    "buyer_email": "jovinerobotics@gmail.com",
    "amount": 1000,
    "webhook_url": "https://jovine.me/zenopay/webhook",
    "billing_country": "TZ",
    "redirect_url": "https://jovine.me/zenopay/redirect",
    "metadata":{
        "product_id": "12345",
        "color": "blue",
        "size": "L",
        "custom_notes": "Please gift-wrap this item."
    },
}

# Initiate a card checkout
checkout=zenopay_client.card_checkout(data)

# Print the response
print(checkout)
#{'status': 'success', 'message': 'Order created successfully', 'order_id': '6777ad7e327xxx', 'payment_link': 'https://secure.payment.tz/link'}
```

You can keep record of the `order_id` to easily keep track of order and update details in case of a callback as the `order_id` will be sent in the callback.

### Check Order Status

```python
status=zenopay_client.check_order_status(order_id="xxxxx")

# Print the response
print(status)
#{"status": "success","order_id": "6777ad7e327xxx","message": "Order status updated","payment_status": "PENDING"}
```

## Callbacks

As highlighted above, you need to set a webhook url when initiating a mobile checkout. Zenopay will send a POST request to the webhook url with the transaction details. You can use the following code to handle the callback.

Sample callback code using Flask and FastAPI. The callback request JSON sample is as follows:

```json
{
    "order_id": "6777ad7e327xxx",
    "payment_status": "COMPLETED",
    "reference": "0882061614",
    "matadata": {
        "product_id": "12345",
        "color": "blue",
        "size": "L",
        "custom_notes": "Please gift-wrap this item."
    }
}
```

- Flask

    ```python
    from flask import Flask, request, jsonify

    app = Flask(__name__)

    @app.route('/zenopay/webhook', methods=['POST'])
    def webhook():
        data = request.json
        # Do something with the data
        print(data)
        # You can save the data to a database
        return jsonify({"status":"success"})

    ```

- FastAPI

    ```python
    from fastapi import FastAPI, Request
    from fastapi.responses import JSONResponse

    app = FastAPI()

    @app.post("/zenopay/webhook")
    async def webhook(request: Request):
        data = await request.json()
        # Do something with the data
        print(data)
        # You can save the data to a database
        return JSONResponse(content={"status":"success"})

    ```

## Redirects and Cancel URLs

These should be set when initiating a card checkout. The redirect url will be used to redirect the user after a successful payment. The cancel url will be used to redirect the user if the payment is cancelled. A provided url will be loaded when either of the two events occur.

Remember both are optional, so setting non-accessible url will hurt the user experience.

## Issues

If you encounter any issues, please open an issue

## Contributing

1. Fork the repository
2. Create a new branch (git checkout -b feature)
3. Make changes
4. Commit your changes (git commit -am 'Add new feature')
5. Push to the branch (git push origin feature)
6. Create a pull request
7. Wait for the PR to be reviewed
