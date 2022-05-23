import requests
from .utils import get_url, get_info
from .token import get_token_list

class Client:
    def __init__(self, everpay_server_url):
        if everpay_server_url.endswith('/'):
            everpay_server_url = everpay_server_url[:-1]
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
    
    def get_token_tag(self, token_symbol):
        token = self.get_token(token_symbol)
        if token:
            return token.get_token_tag()

    def get_token_decimals(self, token_symbol):
        token = self.get_token(token_symbol)
        if token:
            return token.decimals

    def get_support_tokens(self):
        return list(self.get_token_list().keys())

    def get_balance(self, account, token_symbol=''):
        if token_symbol:
            token_tag = self.get_token(token_symbol).get_token_tag()
            path = '/balance/%s/%s' % (token_tag, account)
        else:
            path = '/balances/%s' % account
        url = get_url(self.api_server, path)
        #print(url)
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