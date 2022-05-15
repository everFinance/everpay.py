from sys import api_version
import everpay
api_server = 'https://api-dev.everpay.io'
c = everpay.Client(api_server)
print(c.get_token_list())
print(c.get_support_tokens())
print(c.get_token('eth'))
print(c.get_balance('E1YK40az7mbpAYrdvLNp9PdzacT65DaUeJAkobxskyU', 'ar'))

print()
print('--------------------------')
pk = '9259ecfa1a5e4b494c93985162c84d4d7f7d7d90d62bffa0d855a5981629bfa3'
signer = everpay.ETHSigner(pk)
account = everpay.Account(api_server, signer)
print(account.get_support_tokens())
print(account.get_token('eth'))
print(account.balances())
t, result = account.transfer('usdt', '0x911F42b0229c15bBB38D648B7Aa7CA480eD977d6', 10**6)
print(t.ever_hash)
print(result)