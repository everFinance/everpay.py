import requests, time
def get_token_list(info):
    tokens = {}    
    for t in info['tokenList']:
        symbol = t['symbol']
        token = Token(t['tag'], t['chainType'], t['chainID'], symbol, t['id'], t['decimals'])
        tokens[symbol] = token
    return tokens

class Token:
    def __init__(self, token_tag, chain_type, chain_id, token_symbol, token_id, token_decimals):
        self.token_tag = token_tag
        self.chain_type = chain_type
        self.chain_id = chain_id
        self.symbol = token_symbol
        self.id = token_id
        self.decimals = token_decimals
        
    def __str__(self):
        return 'token %s (%s-%s)'%(self.symbol, self.chain_type, self.chain_id)
    
    def __repr__(self):
        return str(self)