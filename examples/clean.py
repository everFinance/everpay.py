from sys import api_version
import everpay
api_server = 'https://api-dev.everpay.io'
pk = ''
signer = everpay.ETHSigner(pk)
print('account:', signer.address)
account = everpay.Account(api_server, signer)

receiver = '0x61EbF673c200646236B2c53465bcA0699455d5FA'
for b in account.balances()['balances']:
    if b['amount'] != '0':
        amount = b['amount']
        print(b['tag'], amount)
        sym = b['tag'].split('-')[1]
        t, result = account.transfer(sym, receiver, amount)
        print(t.ever_hash)
        print(result)
