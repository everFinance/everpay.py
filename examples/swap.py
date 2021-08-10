import json, time, os, sys
import requests
from everpay.swapIterm import SwapItem

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
sys.path.append(BASE_DIR)
import everpay
from config_kovan import *

everpay_client = everpay.Everpay(everpay_api_host)
pk = open(sender_key_file).read().strip()
sender = everpay.Account(everpay_api_host, sender_address, pk, transfer_fee_recipient)

items = [SwapItem("ethereum-eth-0x0000000000000000000000000000000000000000",
                  "42",
                  sender.address,
                  "0x3314183F9F3CAcf8e4915dA59f754568345aF4D3",
                  "99999"),
         SwapItem("ethereum-eth-0x0000000000000000000000000000000000000000",
                  "42",
                  sender.address,
                  "0x3314183F9F3CAcf8e4915dA59f754568345aF4D3",
                  "99999")
         ]

t, result = sender.swap(sender.address, "ethereum", "42", "eth", "0x0000000000000000000000000000000000000000", items)
print("response:", t, result)
