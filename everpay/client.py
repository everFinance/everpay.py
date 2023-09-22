import requests
from .utils import get_url, get_info, is_token_tag
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
        self.symbol_to_tokens, self.tag_to_tokens = get_token_list(self.info)
        
    def get_info(self):
       return self.info
    
    def get_token(self, token_symbol_or_tag):
        if is_token_tag(token_symbol_or_tag):
            return  self.tag_to_tokens[token_symbol_or_tag]
        
        token_symbol = token_symbol_or_tag
        if not self.symbol_to_tokens.get(token_symbol):
            token_symbol = token_symbol.upper()

        tokens = self.symbol_to_tokens[token_symbol]
        if tokens and len(tokens) == 1:
            return tokens[0]
        
        if tokens and len(tokens) > 1:
            tags = []
            for token in tokens:
                tags.append(token.token_tag)
            tags = "; ".join(tags)
            raise Exception("found multiple tokens (%s) with this symbol (), use token tag instead."%(tags, token_symbol_or_tag))
        
    def get_token_tag(self, token_symbol):
        token = self.get_token(token_symbol)
        if token:
            return token.token_tag

    def get_token_decimals(self, token_symbol_or_tag):
        token = self.get_token(token_symbol_or_tag)
        if token:
            return token.decimals

    def get_token_list(self):
        return self.tag_to_tokens
    
    def get_support_tokens(self):
        return list(self.tag_to_tokens.keys())

    def get_balance(self, account, token_symbol_or_tag=''):
        if token_symbol_or_tag:
            token_tag = token_symbol_or_tag
            if not is_token_tag(token_symbol_or_tag):
                token_tag = self.get_token_tag(token_symbol_or_tag)     
            path = '/balance/%s/%s' % (token_tag, account)
        else:
            path = '/balances/%s' % account
        url = get_url(self.api_server, path)
        return requests.get(url).json()

    def get_txs(self, account='', order='desc', cursor=None):
        path = '/txs'
        if account:
            path = '/txs/%s' % account
        if cursor:
            path = '%s/?order=%s&cursor=%i' % (path, order, int(cursor))
        else:
            path = '%s/?order=%s' % (path, order)
        url = get_url(self.api_server, path)
        return requests.get(url).json()

    def get_tx(self, hash):
        path = '/tx/%s' % hash
        url = get_url(self.api_server, path)
        return requests.get(url).json()