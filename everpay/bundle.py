import json
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
        if item:
            self.add_item(item)

        self.expiration = expiration
        self.salt = salt
        self.version = version
        self.sigs = {}

    def get_data(self):
        sigs = {}
        for k, v in self.sigs.items():
            if is_ar_address(k):
                sigs[k] = v
            else:
                k_ = w3.to_checksum_address(k)
                sigs[k_] = v
                
        self.sigs = sigs
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

def load_bundle(data):
    #{"bundle":{"items":[{"tag":"ethereum-usdt-0xdac17f958d2ee523a2206206994597c13d831ec7","chainID":"1","from":"0xFc772b419846960502089ee43CC66B7312AeFfaD","to":"0xcc7dbEd78e88e79A898d2fe0851F89BB67886a34","amount":"67287759"},{"tag":"arweave,ethereum-ar-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA,0x4fadc7a98f2dc96510e42dd1a74141eeae0c1543","chainID":"0,1","from":"0xcc7dbEd78e88e79A898d2fe0851F89BB67886a34","to":"0xFc772b419846960502089ee43CC66B7312AeFfaD","amount":"2000000000000"}],"expiration":1644912733,"salt":"1bbac9f3-f097-44ea-9ef9-9c6fa85a8a11","version":"v1","sigs":{"0xFc772b419846960502089ee43CC66B7312AeFfaD":"0xc675cf6370a491a8b32a78bcb307b3b334c28772d71dadb7f31e4eb5a8280db11bb3f1e503282e4b96ee9e501ffe8c3ec62529bd0008fe84ec3629680d28001e1b","0xcc7dbEd78e88e79A898d2fe0851F89BB67886a34":"0x088a726ef0edeb882ca5ae207f2c63b6a9ab04cd9437c1118fd33a52a6d9b657613821b119c3f91038b9d80fe2cef85fef4df44b7a82017c3c594630dc8497121c"}}}

    if type(data) == type('bundle'):
        data = json.loads(data)
    
    data = data['bundle']
    bundle = BundleData(None, data['expiration'], data['salt'], data['version'])
    bundle.sigs = data.get('sigs', {})
    for i in data['items']:
        item = BundleItem(i['tag'], i['chainID'], i['from'], i['to'], i['amount'])
        bundle.add_item(item)

    return bundle

def sign_bundle(data_to_sign, address, pk=None, wallet=None):
    
    if is_ar_address(address):
        message = _hash_eip191_message(encode_defunct(text=data_to_sign))
    
        sig = base64url_encode(wallet.sign(message)).decode()
        sig = f'{sig},{wallet.owner}'

    else:
        pk = bytearray.fromhex(pk)
        message = encode_defunct(text=data_to_sign)
        sig = w3.eth.account.sign_message(message, private_key=pk)
        sig = sig.signature.hex()

    return sig


