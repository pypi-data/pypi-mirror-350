from daraja_gateway.token2 import get_access_token
from daraja_gateway.c2b import register_url, simulate_transaction
from daraja_gateway.b2c import send_b2c
from daraja_gateway.b2b import send_b2b
from daraja_gateway.stk_push import initiate_stk_push

class DarajaClient:
    def __init__(self):
        self.token = get_access_token()

    def c2b_register_url(self):
        return register_url(self.token)

    def c2b_simulate(self):
        return simulate_transaction(self.token)

    def b2c_payment(self):
        return send_b2c(self.token)

    def b2b_payment(self):
        return send_b2b(self.token)

    def stk_push(self):
        return initiate_stk_push(self.token)