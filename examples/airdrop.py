import json, time, os, sys
from redis import Redis
import requests
redis_client = Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
sys.path.append(BASE_DIR)
import everpay
from config import *

everpay_client = everpay.Everpay(everpay_api_host)

sleep_time = 2
def get_new_txs(latest_tx_everhash):
    
    result = []
    i = 1
    pages_count = None
    
    while True:
        try:
            data = everpay_client.get_txs(page=i)
        except Exception as e:
            print('Failed to fetch new txs from everpay api server: ', e)
            time.sleep(sleep_time)
            continue
        
        if (not data.get('txs')) or len(data['txs']) == 0:
            return result
        
        if not pages_count:
            pages_count = data['totalPages']
            print('totalPages:', pages_count)

        txs = data['txs']
        print('txs page %i got %i txs.'%(i,len(txs)))
        for t in txs:
            h = t['everHash']
            if h == latest_tx_everhash:
                return result
            else:
                result.append(t)

        if i == pages_count:
            return result

        i = i + 1

def get_weid(address):
    url = '%s/lottery/weid/%s'%(everpay_api_host, address)
    while True:
        try:
            data = requests.get(url).json()
            return data.get('weid')
        except Exception as e:
            print('error when try to get weid of %s'%address, e)
            time.sleep(sleep_time)

pk = open(sender_key_file).read().strip()
sender = everpay.Account(everpay_api_host, sender_address, pk, transfer_fee_recipient)

while True:
    print()
    latest_tx_everhash = redis_client.get('airdrop_latest_tx_everhash')
    print('latest_tx_everhash:', latest_tx_everhash)
    
    txs = get_new_txs(latest_tx_everhash)
    print('get %i new txs'%len(txs))

    txs.reverse()

    for t in txs:
        h = t['everHash']
        redis_client.set('airdrop_latest_tx_everhash', h)

        if t['action'] != 'mint':
            continue
        
        mint_to = t['to']
        print()
        print('get new mint tx:', h, 'mint to:', mint_to)
        
        if redis_client.sismember('airdroped', mint_to):
            print('%s was aridroped'%mint_to)
            continue
        
        mint_weid = get_weid(mint_to)
        if not mint_weid:
            print('failed to get wechat id of %s. next'%mint_to)
            continue

        if redis_client.sismember('airdroped', mint_weid):
            print('%s was aridroped'%mint_to)
            continue
        
        print('try to airdrop to %s %s usdt'%(mint_to, airdrop_amount))

        params = {'app_id': 'airdrop-2021-06'}
        t, result = sender.transfer(mint_to, airdrop_amount * 10**6, 'ethereum', chain_id, 'usdt', data=json.dumps(params))
        print('sent airdrop tx:', t.ever_hash, result)
        try:
            is_ok = json.loads(result)['status']
            if is_ok == 'ok':
                redis_client.sadd('airdroped', mint_weid)
                redis_client.sadd('airdroped', mint_to)
        except Exception as e:
            print('failed to airdrop to %s'%mint_to)

        time.sleep(sleep_time)        
    time.sleep(sleep_time)        
