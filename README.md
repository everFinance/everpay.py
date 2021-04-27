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
api_server = 'https://api-kovan.everpay.io'
e = everpay.Everpay(api_server)
e.get_info()
e.get_balance('0x61EbF673c200646236B2c53465bcA0699455d5FA', 'ethereum', '42', 'eth')
```

- 转账

```python
import everpay
api_server = 'https://api-kovan.everpay.io'
account = everpay.Account(api_server, '0x61EbF673c200646236B2c53465bcA0699455d5FA', '9259ecfa1a5e4b494c93985162c84d4d7f7d7d90d62bffa0d855a5981629bfa3')
account.transfer('0xf9593A9d7F735814B87D08e8D8aD624f58d53B10', 0.001, 'ethereum', '42', 'eth')
```

## todo
- [] deposit/withdraw
