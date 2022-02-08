TOKEN_LIST = [
    #kovan
    ['ethereum', '42', 'eth', '0x0000000000000000000000000000000000000000', 18],
    ['ethereum', '42', 'usdt', '0xd85476c906b5301e8e9eb58d174a6f96b9dfc5ee', 6],

    #mainnet
    ['ethereum', '1', 'eth', '0x0000000000000000000000000000000000000000', 18],
    ['ethereum', '1', 'usdt', '0xdac17f958d2ee523a2206206994597c13d831ec7', 6],
    ['ethereum', '1', 'wbtc', '0x2260fac5e5542a773aa44fbcfedf7c193bc2c599', 8],
    ['ethereum', '1', 'usdc', '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48', 6],
    ['ethereum', '1', 'dai', '0x6b175474e89094c44da98b954eedeac495271d0f', 18],
    ['ethereum', '1', 'uni', '0x1f9840a85d5af5bf1d1762f925bdaddc4201f984', 18],
    ['ethereum', '1', 'sos', '0x3b484b82567a09e2588a13d54d032153f0c0aee0', 18]
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