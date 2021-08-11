import time, os, sys
from web3.auto import w3
from eth_account.messages import encode_defunct
import uuid

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import everpay
from everpay.swap import SwapItem, SwapData

from config import *

everpay_client = everpay.Everpay(everpay_api_host)
pk = open(sender_key_file).read().strip()
sender = everpay.Account(everpay_api_host, sender_address, pk, transfer_fee_recipient)

def sign(pk, message):
    pk = bytearray.fromhex(pk)
    message = encode_defunct(text=message)
    sig = w3.eth.account.sign_message(message, private_key=pk)

    return sig.signature.hex()

def create_uuid():
    return str(uuid.uuid4())

def func1():
    item = SwapItem('ethereum-eth-0x0000000000000000000000000000000000000000',
                    '42',
                    sender.address,
                    '0x3314183F9F3CAcf8e4915dA59f754568345aF4D3',
                    '99999')

    swap_data = SwapData(item, int(time.time() * 1000 + 3000), create_uuid(), 'v1')
    #
    # # item2 = SwapItem('ethereum-eth-0x0000000000000000000000000000000000000000',
    # #                  '42',
    # #                  sender.address,
    # #                  '0x3314183F9F3CAcf8e4915dA59f754568345aF4D3',
    # #                  '99999')
    # #
    # # swap_data.add_item(item2)
    #
    swap_data.sign(sender.address, pk)
    print(sender.swap(sender.address, 'ethereum', '42', 'eth', '0x0000000000000000000000000000000000000000',
                      swap_data.get_data()))

def func2():
    item = SwapItem('ethereum-eth-0x0000000000000000000000000000000000000000',
                    '42',
                    sender.address,
                    '0x3314183F9F3CAcf8e4915dA59f754568345aF4D3',
                    '99999')
    swap_data = SwapData(item, int(time.time() * 1000 + 6000), create_uuid(), 'v1')
    data_to_sign = swap_data.get_data_to_sign()
    sig = sign(pk, data_to_sign)
    # print(sig)
    swap_data.add_sig(sender.address, sig)

    print(sender.swap(sender.address, 'ethereum', '42', 'eth', '0x0000000000000000000000000000000000000000',
                      swap_data.get_data()))

func1()
func2()
