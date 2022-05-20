TOKEN_LIST = [
    #kovan
    ['ethereum', '42', 'eth', '0x0000000000000000000000000000000000000000', 18],
    ['ethereum', '42', 'usdt', '0xd85476c906b5301e8e9eb58d174a6f96b9dfc5ee', 6],
    ['ethereum', '42', 'usdc', '0xb7a4f3e9097c08da09517b5ab877f7a917224ede', 6],

    ['ethereum', '42', 'dai', '0xc4375b7de8af5a38a93548eb8453a498222c4ff2', 18],
    ['arweave', '99', 'pia', 'n05LTiuWcAYjizXAu-ghegaWjL89anZ6VdvuHcU6dno', 18],
    ['arweave', '99', 'vrt', 'usjm4PCxUd5mtaon7zc97-dt-3qf67yPyqgzLnLqk5A', 18],
    ['arweave', '99', 'xyz', 'mzvUgNc8YFk0w5K5H7c8pyT-FC5Y_ba0r7_8766Kx74', 18],
    ['arweave', '99', 'ardrive', '-8A6RexFkpfWwuyVO98wzSFZh0d6VJuI-buTJvlwOJQ', 18],
    ['arweave,ethereum', '0,42', 'ar', 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA,0xcc9141efa8c20c7df0778748255b1487957811be', 12],
    ['moonbase', '1287', 'dev', '0x0000000000000000000000000000000000000000', 18],
    ['moonbase', '1287', 'zlk', '0x322f069e9b8b554f3fb43cefcb0c7b3222242f0e', 18],
    
    ['conflux', '71', 'cfx', '0x0000000000000000000000000000000000000000', 18],

    #mainnet
    ['ethereum', '1', 'eth', '0x0000000000000000000000000000000000000000', 18],
    ['ethereum', '1', 'usdt', '0xdac17f958d2ee523a2206206994597c13d831ec7', 6],
    ['ethereum', '1', 'wbtc', '0x2260fac5e5542a773aa44fbcfedf7c193bc2c599', 8],
    ['ethereum', '1', 'usdc', '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48', 6],
    ['ethereum', '1', 'dai', '0x6b175474e89094c44da98b954eedeac495271d0f', 18],
    ['ethereum', '1', 'uni', '0x1f9840a85d5af5bf1d1762f925bdaddc4201f984', 18],
    ['ethereum', '1', 'sos', '0x3b484b82567a09e2588a13d54d032153f0c0aee0', 18],
    ['ethereum', '1', 'bank', '0x2d94aa3e47d9d5024503ca8491fce9a2fb4da198', 18],
    ['ethereum', '1', 'dodo', '0x43dfc4159d86f3a37a5a4b3d4580b888ad7d4ddd', 18],
    ['ethereum', '1', 'mask', '0x69af81e73a73b40adf4f3d4223cd9b1ece623074', 18],
    ['ethereum', '1', 't4ever', '0xeaba187306335dd773ca8042b3792c46e213636a', 18],

    ['moonbeam', '1284', 'zlk', '0x3fd9b6c9a24e09f67b7b706d72864aebb439100c', 18],
    ['moonbeam', '1284', 'glmr', '0x0000000000000000000000000000000000000000', 18],
    ['arweave,ethereum', '0,1', 'ar', 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA,0x4fadc7a98f2dc96510e42dd1a74141eeae0c1543', 12],
    ['arweave', '0', 'ardrive', '-8A6RexFkpfWwuyVO98wzSFZh0d6VJuI-buTJvlwOJQ', 18],
    ['arweave', '0', 'vrt', 'usjm4PCxUd5mtaon7zc97-dt-3qf67yPyqgzLnLqk5A', 18],

    ['conflux', '1030', 'cfx', '0x0000000000000000000000000000000000000000', 18],
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