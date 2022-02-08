import json
import random
import time, requests
from .utils import get_url
from .transaction import Transaction
from .token import get_token_tag, get_token_decimal, get_token_id

class Everpay:
    def __init__(self, everpay_server_url):
        self.api_server = everpay_server_url

    def get_info(self):
        url = get_url(self.api_server, '/info')
        return requests.get(url).json()

    def get_balance(self, account, chain_type='', chain_id='', token_symbol='', token_id=''):
        if chain_type and chain_id and token_symbol:
            token_tag = get_token_tag(chain_type, chain_id, token_symbol, token_id)
            path = '/balance/%s/%s' % (token_tag, account.lower())
        else:
            path = '/balances/%s' % account.lower()
        url = get_url(self.api_server, path)
        return requests.get(url).json()

    def get_txs(self, account='', order='desc', page=None):
        path = '/txs'
        if account:
            path = '/txs/%s' % account
        if page:
            path = '%s/?order=%s&page=%i' % (path, order, int(page))
        else:
            path = '%s/?order=%s' % (path, order)
        url = get_url(self.api_server, path)
        return requests.get(url).json()

    def get_tx(self, hash):
        path = '/tx/%s' % hash
        url = get_url(self.api_server, path)
        return requests.get(url).json()


class Account:
    def __init__(self, everpay_server_url, address, private_key, ar_wallet, fee_recipient):
        self.everpay = Everpay(everpay_server_url)
        self.address = address
        self.private_key = private_key
        self.ar_wallet = ar_wallet
        self.fee_recipient = fee_recipient

    def get_balance(self, chain_type, chain_id, token_symbol, token_id=''):
        chain_type = chain_type.lower()
        chain_id = str(chain_id).lower()
        token_symbol = token_symbol.lower()
        return self.everpay.get_balance(self.address, chain_type, chain_id, token_symbol, token_id='')

    def get_txs(self):
        return self.everpay.get_txs(self.address)

    def transfer(self, to, amount, chain_type, chain_id, token_symbol, token_id='', data=''):

        chain_type = chain_type.lower()
        chain_id = str(chain_id).lower()
        token_symbol = token_symbol.lower()

        if not token_id:
            token_id = get_token_id(chain_type, chain_id, token_symbol)

        amount_ = str(amount)
        
        if self.ar_wallet and data:
            data = json.loads(data)
            data['arOwner'] = self.ar_wallet.owner
            data = json.dumps(data)
        if self.ar_wallet and not data:
            data = json.dumps({'arOwner': self.ar_wallet.owner})

        t = Transaction(tx_id='', token_symbol=token_symbol, action='transfer', from_=self.address, to=to,
                        amount=amount_, fee='0', fee_recipient=self.fee_recipient, nonce=str(int(time.time() * 1000)),
                        token_id=token_id, chain_type=chain_type, chain_id=chain_id, data=data, version='v1')
        
        if self.private_key:
            t.sign(self.private_key)
        elif self.ar_wallet:
            t.sign_with_ar_wallet(self.ar_wallet)
        else:
            raise Exception('No key or wallet')

        return t, t.post(self.everpay.api_server).content

    def bundle(self, to, chain_type, chain_id, token_symbol, token_id='', data=''):

        chain_type = chain_type.lower()
        chain_id = str(chain_id).lower()
        token_symbol = token_symbol.lower()

        if not token_id:
            token_id = get_token_id(chain_type, chain_id, token_symbol)

        amount_ = '0'
        
        t = Transaction(tx_id='', token_symbol=token_symbol, action='bundle', from_=self.address, to=to,
                        amount=amount_, fee='0', fee_recipient=self.fee_recipient, nonce=str(int(time.time() * 1000)),
                        token_id=token_id, chain_type=chain_type, chain_id=chain_id, data=data, version='v1')
        t.sign(self.private_key)

        return t, t.post(self.everpay.api_server).content
