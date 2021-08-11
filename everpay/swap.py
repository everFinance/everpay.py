from eth_account.messages import encode_defunct
from web3.auto import w3
import json

class SwapItem:
    def __init__(self, token_tag, chain_id, from_, to, amount):
        self.token_tag = token_tag
        self.chain_id = chain_id
        self.from_ = from_
        self.to = to
        self.amount = amount

    def to_dict(self):
        return {
            'tag': self.token_tag,
            'chainID': self.chain_id,
            'from': self.from_,
            'to': self.to,
            'amount': self.amount
        }

class SwapData:
    def __init__(self, item, expiration, salt, version):
        
        self.items = []
        self.add_item(item)

        self.expiration = expiration
        self.salt = salt
        self.version = version
        self.sigs = {}

    def get_data(self):
        data = {
            'swap': {
                'items': [item.to_dict() for item in self.items],
                'expiration': self.expiration,
                'salt': self.salt,
                'version': self.version,
                'sigs': self.sigs,
            }
        }
        return json.dumps(data, separators=(',', ':'), sort_keys=False)

    def get_data_to_sign(self):
        data = {
                'items': [item.to_dict() for item in self.items],
                'expiration': self.expiration,
                'salt': self.salt,
                'version': self.version,
            }

        return json.dumps(data, separators=(',', ':'), sort_keys=False)

    def add_item(self, swap_item):
        if not isinstance(swap_item, SwapItem):
            raise TypeError("swap_item must be a instance of SwapItem")
        self.items.append(swap_item)

    def add_sig(self, address, sig):
        #todo check sig
        self.sigs[address] = sig

    def sign(self, address, pk):
        pk = bytearray.fromhex(pk)
        message = encode_defunct(text=self.get_data_to_sign())
        sig = w3.eth.account.sign_message(message, private_key=pk)
        # print(sig.signature.hex())
        self.sigs[address] = sig.signature.hex()


