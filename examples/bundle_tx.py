import uuid, time, json
import everpay
from everpay import BundleData, BundleItem
# https://docs.everpay.io/docs/guide/dive/bundle
def create_uuid():
    return str(uuid.uuid4())

api_server = 'https://api-dev.everpay.io'
address = '0x61EbF673c200646236B2c53465bcA0699455d5FA'
pk = ''
receiver = '0x911F42b0229c15bBB38D648B7Aa7CA480eD977d6'

signer = everpay.ETHSigner(pk)
account = everpay.Account(api_server, signer)

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

t, result = account.bundle('eth', address, 0, bundle_data.get_data())
print(t.ever_hash)
print('post status:', json.loads(result)['status'])

time.sleep(0.2)
c = account.client
result = c.get_tx(t.ever_hash)
print('internal_status:', result['tx']['internalStatus'] )