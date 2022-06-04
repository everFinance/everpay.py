import requests, time
def get_token_list(info):
    tokens = {}    
    for t in info['tokenList']:
        symbol = t['symbol']
        token = Token(t['chainType'], t['chainID'], symbol, t['id'], t['decimals'])
        tokens[symbol] = token
    return tokens

class Token:
    def __init__(self, chain_type, chain_id, token_symbol, token_id, token_decimals):
        self.chain_type = chain_type
        self.chain_id = chain_id
        self.symbol = token_symbol
        self.id = token_id
        self.decimals = token_decimals
    
    def get_token_tag(self):
        return ('-'.join([self.chain_type, self.symbol.lower(), self.id]))

    def __str__(self):
        return 'token %s (%s-%s)'%(self.symbol, self.chain_type, self.chain_id)
    
    def __repr__(self):
        return str(self)