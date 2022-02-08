# everpay.py

Python wrappers for everpay.io api

Install with

```
pip install everpay
```

## Examples

- 查询

```python
import everpay
api_server = 'https://api-dev.everpay.io'
e = everpay.Everpay(api_server)
e.get_info()
e.get_balance('0x61EbF673c200646236B2c53465bcA0699455d5FA', 'ethereum', '42', 'eth')
```

- 转账

```python
import everpay
api_server = 'https://api-dev.everpay.io'
fee_recipient = '0x6451eB7f668de69Fb4C943Db72bCF2A73DeeC6B1'
address = ''
private_key = ''
receiver = ''
account = everpay.Account(api_server, address, private_key, None, fee_recipient)
account.transfer(receiver, int(0.001 * 10**18), 'ethereum', '42', 'eth')
```

## todo
- [] deposit/withdraw
