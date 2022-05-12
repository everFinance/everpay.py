import json
import time, requests
from .utils import get_url, get_info
from .transaction import Transaction
from .token import get_token_list

class Client:
    def __init__(self, everpay_server_url):
        self.api_server = everpay_server_url
        info_url = get_url(self.api_server, '/info')
        self.info = get_info(info_url)
        self.eth_chain_id = self.info['ethChainID']
        self.fee_recipient = self.info['feeRecipient']
        self.token_list = get_token_list(self.info)
        
    def get_info(self):
       return self.info
    
    def get_token_list(self):
        return self.token_list
    
    def get_token(self, token_symbol):
        return self.token_list[token_symbol.upper()]

    def get_support_tokens(self):
        return list(self.get_token_list().keys())

    def get_balance(self, account, token_symbol=''):
        if token_symbol:
            token_tag = self.get_token(token_symbol).get_token_tag()
            path = '/balance/%s/%s' % (token_tag, account)
        else:
            path = '/balances/%s' % account
        url = get_url(self.api_server, path)
        print(url)
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
    def __init__(self, everpay_server_url, signer):
        self.client = Client(everpay_server_url)
        self.address = signer.address
        self.signer = signer
       
    def get_balance(self, token_symbol=''):
        return self.client.get_balance(self.address, token_symbol)

    def get_txs(self):
        return self.client.get_txs(self.address)
    
    def get_transfer_fee(self):
        return 0

    def transfer(self, token_symbol, to, amount, data=''):

        token = self.client.get_token(token_symbol)
        fee = self.get_transfer_fee()

        if self.signer.type == 'AR' and data:
            data = json.loads(data)
            data['arOwner'] = self.signer.owner
            data = json.dumps(data)
        if self.signer.type == 'AR' and not data:
            data = json.dumps({'arOwner': self.signer.owner})

        t = Transaction(tx_id='', token_symbol=token_symbol, action='transfer', from_=self.address, to=to,
                        amount=str(amount), fee=str(fee), fee_recipient=self.client.fee_recipient, nonce=str(int(time.time() * 1000)),
                        token_id=token.id, chain_type=token.chain_type, chain_id=token.chain_id, data=data, version='v1')
        
        t.sig = self.signer.sign(str(t))
        
        return t, t.post(self.client.api_server).content

    def bundle(self, token_symbol, to, data=''):

        token = self.client.get_token(token_symbol)
        amount_ = '0'
        
        t = Transaction(tx_id='', token_symbol=token_symbol, action='bundle', from_=self.address, to=to,
                        amount=amount_, fee='0', fee_recipient=self.fee_recipient, nonce=str(int(time.time() * 1000)),
                        token_id=token.token_id, chain_type=token.chain_type, chain_id=token.chain_id, data=data, version='v1')
        t.sign(self.private_key)

        return t, t.post(self.client.api_server).content
