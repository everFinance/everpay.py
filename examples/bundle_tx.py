import time, uuid, json
import everpay as everpay
from everpay.bundle import BundleItem, BundleData

# https://docs.everpay.io/docs/guide/dive/bundle
def create_uuid():
    return str(uuid.uuid4())

api_server = 'https://api-dev.everpay.io'
fee_recipient = '0x6451eB7f668de69Fb4C943Db72bCF2A73DeeC6B1'

address = '0x61EbF673c200646236B2c53465bcA0699455d5FA'
pk = '9259ecfa1a5e4b494c93985162c84d4d7f7d7d90d62bffa0d855a5981629bfa3'
receiver = '0x258D9aeF9184d9e21f9b882E243c42fAC1466A59'

account = everpay.Account(api_server, address, pk, None, fee_recipient)

bundle_item = BundleItem('ethereum-eth-0x0000000000000000000000000000000000000000',
                    '42',
                    address,
                    receiver,
                    str(10**16)
                )
bundle_data = BundleData(bundle_item, int( time.time() + 100), create_uuid(), 'v1')

bundle_item2 = BundleItem('ethereum-usdt-0xd85476c906b5301e8e9eb58d174a6f96b9dfc5ee',
                    '42',
                    address,
                    receiver,
                    str(10**5)
                )

bundle_data.add_item(bundle_item2)
bundle_data.sign(address, pk)

t, result = account.bundle(address, 'ethereum', '42', 'eth', 
                        '0x0000000000000000000000000000000000000000',
                        bundle_data.get_data())
print(t.ever_hash)
print('post status:', json.loads(result)['status'])

time.sleep(0.2)
e = everpay.Everpay(api_server)
result = e.get_tx(t.ever_hash)
print('internal_status:', result['tx']['internalStatus'] )