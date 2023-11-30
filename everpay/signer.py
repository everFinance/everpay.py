import hashlib
import arweave
from eth_account import Account
from web3.auto import w3
from eth_account.messages import encode_defunct, _hash_eip191_message
from jose.utils import base64url_encode
class ETHSigner:
    def __init__(self, private_key):
        self.type = 'ETH'
        if private_key.startswith('0x'):
            private_key = private_key[:2]
        self.private_key = private_key
        self.address = Account.from_key(self.private_key).address

    def sign(self, msg):
        pk = bytearray.fromhex(self.private_key)
        if type(msg) == type(""):
            message = encode_defunct(text=msg)
        elif type(msg) == type(b""):
            message = encode_defunct(primitive=msg)
        else:
            raise ValueError("Invalid msg")  
        sig = w3.eth.account.sign_message(message, private_key=pk)
        return sig.signature.hex()
    
    def sign_bundle(self, msg):
        return self.sign(msg)

class ARSigner:
    def __init__(self, arwallet_file_path):
        self.type = 'AR'
        self.wallet = arweave.Wallet(arwallet_file_path)
        self.address = self.wallet.address
        self.owner = self.wallet.owner

    def sign(self, msg):
        h = hashlib.sha256(msg.encode()).digest()
        sig = base64url_encode(self.wallet.sign(h)).decode()
        return sig
    
    def sign_bundle(self, msg):
        sig = self.sign(msg)
        sig = f'{sig},{self.owner}'
        return sig