from eth_account.messages import encode_defunct
from web3.auto import w3
import json


class SwapData:
    def __init__(self, items, expiration, salt, version):
        self.items = []
        self.items.append(items)
        self.expiration = expiration
        self.salt = salt
        self.version = version
        self.sigs = {}

    def get_data(self):
        data = {
            "swap": {
                "items": [item.getter() for item in self.items],
                "expiration": self.expiration,
                "salt": self.salt,
                "version": self.version,
                "sigs": self.sigs,
            }
        }
        return json.dumps(data, separators=(',', ':'), sort_keys=False)

    def get_sign_data(self):
        data = {
                "items": [item.getter() for item in self.items],
                "expiration": self.expiration,
                "salt": self.salt,
                "version": self.version,
            }

        return json.dumps(data, separators=(',', ':'), sort_keys=False)

    def add_item(self, item):
        print(self.items)
        self.items.append(item)
        print(self.items)

    def add_sig(self, address, sig):
        self.sigs[address] = sig


    def sign(self, address, pk):
        pk = bytearray.fromhex(pk)
        message = encode_defunct(text=self.get_sign_data())
        sig = w3.eth.account.sign_message(message, private_key=pk)
        # print(sig.signature.hex())
        self.sigs[address] = sig.signature.hex()


class SwapItem:
    def __init__(self, tag, chain_id, from_, to, amount):
        self.tag = tag
        self.chain_id = chain_id
        self.from_ = from_
        self.to = to
        self.amount = amount

    def getter(self):
        return {
            "tag": self.tag,
            "chainID": self.chain_id,
            "from": self.from_,
            "to": self.to,
            "amount": self.amount
        }
