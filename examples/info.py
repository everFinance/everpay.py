import everpay

c = everpay.Client('https://api.everpay.io')
print(c.get_token_list())
print(c.get_support_tokens())
print(c.get_token('eth'))