import everpay
api_server = 'https://api.everpay.io'
pk = ''
signer = everpay.ETHSigner(pk)
print('account:', signer.address)
account = everpay.Account(api_server, signer)

receiver = '0xfc772b419846960502089ee43cc66b7312aeffad'
for b in account.balances()['balances']:
    if b['amount'] != '0':
        amount = b['amount']
        print(b['tag'], amount)
        sym = b['tag'].split('-')[1]
        t, result = account.transfer(sym, receiver, amount)
        print(t.ever_hash)
        print(result)
