import time, json
from .transaction import Transaction
from .client import Client

class Account(Client):
    def __init__(self, everpay_server_url, signer):
        super().__init__(everpay_server_url)
        self.address = signer.address
        self.signer = signer
     
    def get_transfer_fee(self):
        return 0

    def balances(self):
        return self.get_balance(self.address)
    
    def sign(self, msg):
        return self.signer.sign(msg)

    def send_tx(self, action, token_symbol, to, amount, data):
        token = self.get_token(token_symbol)
        fee = self.get_transfer_fee()

        if self.signer.type == 'AR' and data:
            data = json.loads(data)
            data['arOwner'] = self.signer.owner
            data = json.dumps(data)
        if self.signer.type == 'AR' and not data:
            data = json.dumps({'arOwner': self.signer.owner})

        t = Transaction(tx_id='', token_symbol=token_symbol, action=action, from_=self.address, to=to,
                        amount=str(amount), fee=str(fee), fee_recipient=self.fee_recipient, nonce=str(int(time.time() * 1000)),
                        token_id=token.id, chain_type=token.chain_type, chain_id=token.chain_id, data=data, version='v1')
        
        t.sig = self.signer.sign(str(t))
        
        return t, t.post(self.api_server).content

    def transfer(self, token_symbol, to, amount, data=''):
        return self.send_tx('transfer', token_symbol, to, amount, data)
    
    def bundle(self, token_symbol, to, amount, data):
        return self.send_tx('bundle', token_symbol, to, amount, data)