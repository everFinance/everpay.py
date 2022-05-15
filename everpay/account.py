import time, json
from .transaction import Transaction
from .client import Client

class Account:
    def __init__(self, everpay_server_url, signer):
        self.client = Client(everpay_server_url)
        self.address = signer.address
        self.signer = signer
    
    def get_support_tokens(self):
        return self.client.get_support_tokens()
        
    def get_balance(self, token_symbol=''):
        return self.client.get_balance(self.address, token_symbol)

    def get_txs(self):
        return self.client.get_txs(self.address)
    
    def get_transfer_fee(self):
        return 0

    def send_tx(self, action, token_symbol, to, amount, data):
        token = self.client.get_token(token_symbol)
        fee = self.get_transfer_fee()

        if self.signer.type == 'AR' and data:
            data = json.loads(data)
            data['arOwner'] = self.signer.owner
            data = json.dumps(data)
        if self.signer.type == 'AR' and not data:
            data = json.dumps({'arOwner': self.signer.owner})

        t = Transaction(tx_id='', token_symbol=token_symbol, action=action, from_=self.address, to=to,
                        amount=str(amount), fee=str(fee), fee_recipient=self.client.fee_recipient, nonce=str(int(time.time() * 1000)),
                        token_id=token.id, chain_type=token.chain_type, chain_id=token.chain_id, data=data, version='v1')
        
        t.sig = self.signer.sign(str(t))
        
        return t, t.post(self.client.api_server).content

    def transfer(self, token_symbol, to, amount, data=''):
        return self.send_tx('transfer', token_symbol, to, amount, data)
    
    def bundle(self, token_symbol, to, amount, data):
        return self.send_tx('bundle', token_symbol, to, amount, data)