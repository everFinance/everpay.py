import json
import random
import time, requests
from .utils import get_url
from .transaction import Transaction
from .token import get_token_tag, get_token_decimal, get_token_id
from .swapIterm import SwapItem
from web3.auto import w3
from eth_account.messages import encode_defunct, _hash_eip191_message

class Everpay:
    def __init__(self, everpay_server_url):
        self.api_server = everpay_server_url

    def get_info(self):
        url = get_url(self.api_server, '/info')
        return requests.get(url).json()

    def get_balance(self, account, chain_type='', chain_id='', token_symbol='', token_id=''):
        if chain_type and chain_id and token_symbol:
            token_tag = get_token_tag(chain_type, chain_id, token_symbol, token_id)
            path = '/balance/%s/%s' % (token_tag, account.lower())
        else:
            path = '/balances/%s' % account.lower()
        url = get_url(self.api_server, path)
        return requests.get(url).json()

    def get_txs(self, account='', order='desc', page=None):
        path = '/txs'
        if account:
            path = '/txs/%s' % account
        if page:
            path = '%s/?order=%s&page=%i' % (path, order, int(page))
        else:
            path = '%s/?order=%s' % (path, order)
        url = get_url(self.api_server, path)
        return requests.get(url).json()

    def get_tx(self, hash):
        path = '/tx/%s' % hash
        url = get_url(self.api_server, path)
        return requests.get(url).json()


class Account:
    def __init__(self, everpay_server_url, address, private_key, fee_recipient=''):
        self.everpay = Everpay(everpay_server_url)
        self.address = address
        self.private_key = private_key
        self.fee_recipient = fee_recipient

    def get_balance(self, chain_type, chain_id, token_symbol, token_id=''):
        chain_type = chain_type.lower()
        chain_id = str(chain_id).lower()
        token_symbol = token_symbol.lower()
        return self.everpay.get_balance(self.address, chain_type, chain_id, token_symbol, token_id='')

    def get_txs(self):
        return self.everpay.get_txs(self.address)

    def transfer(self, to, amount, chain_type, chain_id, token_symbol, token_id='', data=''):

        chain_type = chain_type.lower()
        chain_id = str(chain_id).lower()
        token_symbol = token_symbol.lower()

        if not token_id:
            token_id = get_token_id(chain_type, chain_id, token_symbol)
        decimal = get_token_decimal(chain_type, chain_id, token_symbol)
        amount_ = str(amount)
        t = Transaction(tx_id='', token_symbol=token_symbol, action='transfer', from_=self.address, to=to,
                        amount=amount_, fee='0', fee_recipient=self.fee_recipient, nonce=str(int(time.time() * 1000)),
                        token_id=token_id, chain_type=chain_type, chain_id=chain_id, data=data, version='v1')
        t.sign(self.private_key)
        return t, t.post(self.everpay.api_server).content

    def swap(self, to, chain_type, chain_id, token_symbol, token_id='', items=None):

        if items is None:
            items = []

        for item in items:
            if not isinstance(item,SwapItem):
                raise Exception(item, 'wrong items')

        chain_type = chain_type.lower()
        chain_id = str(chain_id).lower()
        token_symbol = token_symbol.lower()

        if not token_id:
            token_id = get_token_id(chain_type, chain_id, token_symbol)

        amount_ = '0'

        #     "expiration": 162851932400,
        #     "salt": "9988",
        #     "version": "v1",
        #     "sigs": {
        #       "0x3314183F9F3CAcf8e4915dA59f754568345aF4D3": "0x229827382c6e1a440de7dbf4d679ea11449a592f213de8e869f906e5dc3a0368645900892a0f44a99d18546c16428c722dff8807cf045fe424dfb380a16a5db11c",
        #       "0xa06b79E655Db7D7C3B3E7B2ccEEb068c3259d0C9": "0x063f73af716d02e98f6844a928881dfe2c9f1393e6f3785abaf2afc6210fc28e5a02dc634772f1879f380fa5ab23553b18cf21891b68f953a50177c8271657871b"
        #     }

        items = [item.getter() for item in items]
        expiration = int(time.time()*1000 + 60000)
        slat = str(time.time())

        dict_to_sig = {
            "swap": {
                "items": items,
                "expiration": expiration,
                "salt": slat,
                "version": "v1",
            }
        }

        data = json.dumps(dict_to_sig["swap"],separators=(',',':'),sort_keys=False)
        # print("data to sign", data)
        sig = self.sign(data)

        dict_signed = {
            "swap": {
                "items": items,
                "expiration": expiration,
                "salt": slat,
                "version": "v1",
                "sigs": {self.address: sig},
            }
        }
        data = json.dumps(dict_signed,separators=(',',':'),sort_keys=False)
        # print("data to send", data)

        print(data)
        t = Transaction(tx_id='', token_symbol=token_symbol, action='aswap', from_=self.address, to=to,
                        amount=amount_, fee='0', fee_recipient=self.fee_recipient, nonce=str(int(time.time() * 1000)),
                        token_id=token_id, chain_type=chain_type, chain_id=chain_id, data=data, version='v1')
        t.sign(self.private_key)
        return t, t.post(self.everpay.api_server).content

    def sign(self,message):
        pk = bytearray.fromhex(self.private_key)
        message = encode_defunct(text=message)
        sig = w3.eth.account.sign_message(message, private_key=pk)
        return sig.signature.hex()
