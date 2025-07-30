import base64
import requests
import logging
from daraja_gateway.config import CONSUMER_KEY, CONSUMER_SECRET, BASE_URL

logger = logging.getLogger(__name__)

def get_access_token():
    try:
        credentials = f"{CONSUMER_KEY}:{CONSUMER_SECRET}"
        encoded = base64.b64encode(credentials.encode()).decode()
        headers = {"Authorization": f"Basic {encoded}"}
        response = requests.get(f"{BASE_URL}/oauth/v1/generate?grant_type=client_credentials", headers=headers)
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.RequestException as e:
        logger.error(f"Failed to get access token: {e}")
        return None