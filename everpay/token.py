TOKEN_LIST = [
    ['ethereum', '42', 'eth', '0x0000000000000000000000000000000000000000', 18],
    ['ethereum', '42', 'usdt', '0xd85476c906b5301e8e9eb58d174a6f96b9dfc5ee', 6]
]

def get_token_id(chain_type, chain_id, token_symbol):
    for token in TOKEN_LIST:
        if token[0] == chain_type and token[1] == chain_id and token[2] == token_symbol:
            return token[3]

def get_token_decimal(chain_type, chain_id, token_symbol):
    for token in TOKEN_LIST:
        if token[0] == chain_type and token[1] == chain_id and token[2] == token_symbol:
            return token[4]
    
def get_token_tag(chain_type, chain_id, token_symbol, token_id=''):
    if not token_id:
        token_id = get_token_id(chain_type, chain_id, token_symbol)

    return '-'.join([chain_type, token_symbol, token_id])

