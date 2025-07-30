# Daraja Gateway

This library provides integration with the Safaricom Daraja API using Flask.

## Features
- OAuth token management
- C2B, B2C, B2B, STK Push
- Webhook validation and confirmation

## Installation
```bash
pip install .
```

## Environment Configuration
Create a `.env` file in the root of your project:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
CONSUMER_KEY=your_consumer_key
CONSUMER_SECRET=your_consumer_secret
BASE_URL=https://sandbox.safaricom.co.ke
SHORT_CODE=600000
PASSKEY=your_passkey
INITIATOR_NAME=testapi
SECURITY_CREDENTIAL=your_encoded_security_credential
CALLBACK_URL=https://yourdomain.com/webhook/confirmation
VALIDATION_URL=https://yourdomain.com/webhook/validation
PARTY_B=600000
```

## Usage
```python
from daraja_gateway.client import DarajaClient
client = DarajaClient()
response = client.stk_push()
print(response)
```
