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
    
    def sign_bundle(self, msg):
        return self.signer.sign_bundle(msg)

    def send_tx(self, action, token_symbol_or_tag, to, amount, data, is_dry_run):
        token = self.get_token(token_symbol_or_tag)
        fee = self.get_transfer_fee()

        if self.signer.type == 'AR' and data:
            data = json.loads(data)
            data['arOwner'] = self.signer.owner
            data = json.dumps(data)
        if self.signer.type == 'AR' and not data:
            data = json.dumps({'arOwner': self.signer.owner})

        t = Transaction(tx_id='', token_symbol=token.symbol, action=action, from_=self.address, to=to,
                        amount=str(amount), fee=str(fee), fee_recipient=self.fee_recipient, nonce=str(int(time.time() * 1000)),
                        token_id=token.id, chain_type=token.chain_type, chain_id=token.chain_id, data=data, version='v1')
        
        t.sig = self.signer.sign(str(t))
        
        if is_dry_run:
            return t

        return t, t.post(self.api_server).content

    def transfer(self, token_symbol_or_tag, to, amount, data='', is_dry_run=False):
        return self.send_tx('transfer', token_symbol_or_tag, to, amount, data, is_dry_run)
    
    def bundle(self, token_symbol_or_tag, to, amount, data, is_dry_run=False):
        return self.send_tx('bundle', token_symbol_or_tag, to, amount, data, is_dry_run)