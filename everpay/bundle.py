from jose.utils import base64url_encode
from web3.auto import w3
from eth_account.messages import encode_defunct, _hash_eip191_message
import json
from .utils import *

class BundleItem:
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

class BundleData:
    def __init__(self, item, expiration, salt, version):
        
        self.items = []
        self.add_item(item)

        self.expiration = expiration
        self.salt = salt
        self.version = version
        self.sigs = {}

    def get_data(self):
        data = {
            'bundle': {
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

    def get_hash_message(self):
        #print('msg:', self.get_data_to_sign())
        return _hash_eip191_message(encode_defunct(text=self.get_data_to_sign()))
    
    def get_sigs(self):
        return self.sigs

    def add_item(self,item):
        if not isinstance(item, BundleItem):
            raise TypeError('item must be a instance of BundleItem')
        self.items.append(item)

    def add_sig(self, address, sig):
        if is_ar_address(address):
            sig_, owner = sig.split(',')
            
            if owner_to_address(owner) != address:
                raise ValueError('invalid signature: address is not from owner')
            message = self.get_data_to_sign()
            if not verify_ar_sig(owner, message, sig_):
                raise ValueError('invalid signature')

            self.sigs[address] = sig
        else:
            message = encode_defunct(text=self.get_data_to_sign())
            sign_address = w3.eth.account.recover_message(message, signature=sig)

            if sign_address.lower() != address.lower():
                raise ValueError('invalid signature')
            self.sigs[address] = sig

    def sign(self, address, pk=None, wallet=None):
        if is_ar_address(address):
            message = self.get_hash_message()
            sig = base64url_encode(wallet.sign(message)).decode()
            sig = f'{sig},{wallet.owner}'

            self.add_sig(address, sig)
        else:
            pk = bytearray.fromhex(pk)
            message = encode_defunct(text=self.get_data_to_sign())
            sig = w3.eth.account.sign_message(message, private_key=pk)
            self.add_sig(address, sig.signature.hex())
        # print(sig.signature.hex())




