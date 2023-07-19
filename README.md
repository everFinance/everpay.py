# everpay.py

Python wrappers for everpay.io [api](https://docs.everpay.io/).

Install with

```
pip install everpay
```

## v0.1.x 
v0.1.x version api example [v0.1.x](./docs/v0.1.x.md)

## Examples

- query

```python
import everpay
api_server = 'https://api-dev.everpay.io'
c = everpay.Client(api_server)
print(c.get_info())
print(c.get_token_list())
print(c.get_support_tokens())
c.get_balance('0x61EbF673c200646236B2c53465bcA0699455d5FA', 'eth')
c.get_balance('0x61EbF673c200646236B2c53465bcA0699455d5FA', 'ar')

```

- transfer

```python
import everpay
api_server = 'https://api-dev.everpay.io'

pk = ''
#eth account
signer = everpay.ETHSigner(pk)
#ar account
#signer = everpay.ARSigner('arweave-keyfile-xxx.json')
account = everpay.Account(api_server, signer)
t, result = account.transfer('usdt', '0x911F42b0229c15bBB38D648B7Aa7CA480eD977d6', 10**6)
print(t.ever_hash)
print(result)

```

- bundle

see example/bundle_tx.py

- token symbol or tag

sometimes two token may have same token symbol in everpay. for example, usdc bridged from ethereum and usdc bridged from bsc have the same token symbol "usdc". 

In this case, you should use token tag, which is always unique in everpay, to call api function.

```python

import everpay
api_server = 'https://api-dev.everpay.io'
c = everpay.Client(api_server)

# get token tag list
print(c.get_token_list())

# get balance of usdc bridged from bsc
c.get_balance('0x61EbF673c200646236B2c53465bcA0699455d5FA', 'bsc-usdc-0x64544969ed7ebf5f083679233325356ebe738930')
# get balance of usdc bridged from ethereum
c.get_balance('0x61EbF673c200646236B2c53465bcA0699455d5FA', 'ethereum-usdc-0xf044320bcc3cd1f6100cd197754c71941469e79c')

```

## todo
- [] deposit/withdraw
