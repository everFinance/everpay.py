import everpay
api_server = 'https://api-dev.everpay.io'
c = everpay.Client(api_server)
print(c.get_token_list())
print(c.get_support_tokens())
print(c.get_token('eth'))
print(c.get_token_tag('usdt'))
print(c.get_token_decimals('ar'))

print(c.get_balance('E1YK40az7mbpAYrdvLNp9PdzacT65DaUeJAkobxskyU', 'ar'))

print()
print('--------------------------')
pk = ''
signer = everpay.ETHSigner(pk)
account = everpay.Account(api_server, signer)
print(account.get_support_tokens())
print(account.get_token('eth'))
print(account.balances())
t, result = account.transfer('usdt', '0x911F42b0229c15bBB38D648B7Aa7CA480eD977d6', 10**6)
print(t.ever_hash)
print(result)