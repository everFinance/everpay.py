import time, requests
from decimal import Decimal
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
        if chain_type and chain_id and token_symbol and token_id:
            token_tag = get_token_tag(chain_type, chain_id, token_symbol, token_id='')
            path = '/balanceOf/%s/%s'%(token_tag, account.lower())
        else:
            path = '/balances/%s'%account.lower()
        url = get_url(self.api_server, path)
        return requests.get(url).json()

    def get_txs(self, account='', hash=''):
        path = '/txs'
        if account:
            path = '/txs/%s'%account
        if hash:
            path = '/txs/%s'%hash
        url = get_url(self.api_server, path)
        return requests.get(url).json()

class Account:
    def __init__(self, everpay_server_url, address, private_key):
        self.everpay = Everpay(everpay_server_url)
        self.address = address
        self.private_key = private_key
    
    def get_balance(self, chain_type, chain_id, token_symbol, token_id=''):
        return self.everpay.get_balance(self.address, chain_type, chain_id, token_symbol, token_id='')
    
    def get_txs(self):
        return self.everpay.get_txs(self.address)
    
    def transfer(self, to, amount, chain_type, chain_id, token_symbol, token_id='', data=''):
        if not token_id:
            token_id = get_token_id(chain_type, chain_id, token_symbol)
        #decimal = get_token_decimal(chain_type, chain_id, token_symbol)
        amount_ = str(amount)
        t = Transaction(tx_id='', token_symbol=token_symbol, action='transfer', from_=self.address, to=to, 
                         amount=amount_, fee='0', fee_recipient='', nonce=str(int(time.time() * 1000)), 
                         token_id=token_id, chain_type=chain_type, chain_id=chain_id, data=data, version='v1')
        t.sign(self.private_key)
        return t.post(self.everpay.api_server).content


