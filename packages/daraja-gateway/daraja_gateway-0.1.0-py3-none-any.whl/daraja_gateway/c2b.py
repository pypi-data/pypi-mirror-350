import requests
import logging
from daraja_gateway.config import BASE_URL, SHORT_CODE, CALLBACK_URL, VALIDATION_URL

logger = logging.getLogger(__name__)

def register_url(token):
    url = f"{BASE_URL}/mpesa/c2b/v1/registerurl"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "ShortCode": SHORT_CODE,
        "ResponseType": "Completed",
        "ConfirmationURL": CALLBACK_URL,
        "ValidationURL": VALIDATION_URL
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"C2B register URL failed: {e}")
        return None

def simulate_transaction(token):
    url = f"{BASE_URL}/mpesa/c2b/v1/simulate"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "ShortCode": SHORT_CODE,
        "CommandID": "CustomerPayBillOnline",
        "Amount": 100,
        "Msisdn": "254700000000",
        "BillRefNumber": "TestBill"
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"C2B simulate transaction failed: {e}")
        return None
