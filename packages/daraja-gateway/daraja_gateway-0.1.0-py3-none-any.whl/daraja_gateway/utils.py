import datetime
import base64
from daraja_gateway.config import SHORT_CODE, PASSKEY

def get_timestamp():
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

def generate_password():
    timestamp = get_timestamp()
    data_to_encode = SHORT_CODE + PASSKEY + timestamp
    return base64.b64encode(data_to_encode.encode()).decode(), timestamp
