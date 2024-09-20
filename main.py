import aiohttp
import asyncio
import base64
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

client_id = os.getenv("PAYPAL_CLIENT_ID")
secret = os.getenv("PAYPAL_SECRET")

async def get_paypal_token(client_id, secret, url):
    auth = base64.b64encode(f"{client_id}:{secret}".encode()).decode("utf-8")
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    body = {
        "grant_type": "client_credentials"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=body) as response:
            return await response.json()

async def create_payment(url, access_token, payload):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            return await response.json()

async def main():
    paypal_url = "https://api.sandbox.paypal.com/v1/oauth2/token"
    token_response = await get_paypal_token(client_id, secret, paypal_url)
    access_token = token_response.get("access_token")

    payment_url = "https://api.sandbox.paypal.com/v1/payments/payment"
    payment_payload = {
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "transactions": [{
            "amount": {
                "total": "30.11",
                "currency": "USD"
            },
            "description": "This is the payment transaction description."
        }],
        "redirect_urls": {
            "return_url": "http://example.com/your_redirect_url/",
            "cancel_url": "http://example.com/your_cancel_url/"
        }
    }
    payment_response = await create_payment(payment_url, access_token, payment_payload)
    print(payment_response)

if __name__ == "__main__":
    asyncio.run(main())