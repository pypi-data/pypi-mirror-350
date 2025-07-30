import requests
import logging
from daraja_gateway.config import BASE_URL, SHORT_CODE, CALLBACK_URL
from daraja_gateway.utils import generate_password

logger = logging.getLogger(__name__)

def initiate_stk_push(token):
    url = f"{BASE_URL}/mpesa/stkpush/v1/processrequest"
    password, timestamp = generate_password()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "BusinessShortCode": SHORT_CODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": "254700000000",
        "PartyB": SHORT_CODE,
        "PhoneNumber": "254700000000",
        "CallBackURL": CALLBACK_URL,
        "AccountReference": "TestAccount",
        "TransactionDesc": "STK Push Test"
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"STK Push failed: {e}")
        return None
