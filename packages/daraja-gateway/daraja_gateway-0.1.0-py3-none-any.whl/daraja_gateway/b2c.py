import requests
import logging
from daraja_gateway.config import BASE_URL, SECURITY_CREDENTIAL, INITIATOR_NAME, SHORT_CODE, CALLBACK_URL, PARTY_B

logger = logging.getLogger(__name__)

def send_b2c(token):
    url = f"{BASE_URL}/mpesa/b2c/v1/paymentrequest"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "InitiatorName": INITIATOR_NAME,
        "SecurityCredential": SECURITY_CREDENTIAL,
        "CommandID": "BusinessPayment",
        "Amount": 100,
        "PartyA": SHORT_CODE,
        "PartyB": PARTY_B,
        "Remarks": "B2C Payment",
        "QueueTimeOutURL": CALLBACK_URL,
        "ResultURL": CALLBACK_URL,
        "Occasion": "Test"
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"B2C payment failed: {e}")
        return None