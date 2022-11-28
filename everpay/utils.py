import hashlib, requests, time

from jose.utils import base64url_decode, base64url_encode
from jose import jwk
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA256
from eth_account.messages import encode_defunct, _hash_eip191_message
from Crypto.PublicKey import RSA

def get_url(server, path):
    if server.endswith('/'):
        return server[:-1] + path
    return server + path

def is_ar_address(address):
    if len(address) != 43:
        return False
    try:
        base64url_decode(address.encode())
    except:
        return False
    return True

def eip191_hash(message):
    return _hash_eip191_message(encode_defunct(text=message))

def verify_ar_sig(owner, message, sig):
    data = {'kty':'RSA', 'e':"AQAB", 'n':owner}
    jwk_ = jwk.construct(data, algorithm=jwk.ALGORITHMS.RS256)
    public_key = RSA.importKey(jwk_.to_pem())
    hash_ = SHA256.new(eip191_hash(message))
    sig = base64url_decode(sig.encode())
    #return PKCS1_PSS.new(public_key, saltLen=32).verify(hash_, sig)
    return PKCS1_PSS.new(public_key).verify(hash_, sig)

def owner_to_address(owner):
    result = base64url_encode(hashlib.sha256(base64url_decode(owner.encode('ascii'))).digest()).decode()
    return result

def get_info(info_url):
    for i in range(3):
        try:
            return requests.get(info_url).json()
        except:
            time.sleep(0.2)
            continue
    raise ValueError('failed to get info')

def is_token_tag(token_symbol_or_tag):
    if token_symbol_or_tag.find('-') != -1:
        return True
    return False