import os
from dotenv import load_dotenv

load_dotenv()

CONSUMER_KEY = os.getenv('CONSUMER_KEY', 'your_consumer_key')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET', 'your_consumer_secret')
BASE_URL = os.getenv('BASE_URL', 'https://sandbox.safaricom.co.ke')

SHORT_CODE = os.getenv('SHORT_CODE', '600000')
PASSKEY = os.getenv('PASSKEY', 'your_passkey')
INITIATOR_NAME = os.getenv('INITIATOR_NAME', 'testapi')
SECURITY_CREDENTIAL = os.getenv('SECURITY_CREDENTIAL', 'your_encoded_security_credential')
CALLBACK_URL = os.getenv('CALLBACK_URL', 'https://yourdomain.com/webhook/confirmation')
VALIDATION_URL = os.getenv('VALIDATION_URL', 'https://yourdomain.com/webhook/validation')
PARTY_B = os.getenv('PARTY_B', '600000')