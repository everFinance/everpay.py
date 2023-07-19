import requests
from web3.auto import w3
from eth_account.messages import encode_defunct, _hash_eip191_message

class Transaction:
    def __init__(self, tx_id, token_symbol, action, from_, to, amount, 
                    fee, fee_recipient, nonce, token_id, chain_type, chain_id, data, version):
        self.tx_id = tx_id
        self.token_symbol = token_symbol
        self.action = action
        self.from_ = from_
        self.to = to
        self.amount = amount
        self.fee = fee
        self.fee_recipient = fee_recipient
        self.nonce = nonce
        self.token_id = token_id
        self.chain_type = chain_type
        self.chain_id = chain_id
        self.data = data
        self.version = version
        self.sig = ''
        self.ever_hash = self.get_ever_hash()

    def __str__(self):
        return 'tokenSymbol:' + self.token_symbol + '\n' + \
                'action:' + self.action + '\n' + \
                'from:' + self.from_ + '\n' + \
                'to:' + self.to + '\n' + \
                'amount:' + self.amount + '\n' + \
                'fee:' + self.fee + '\n' + \
                'feeRecipient:' + self.fee_recipient + '\n' + \
                'nonce:' + self.nonce + '\n' + \
                'tokenID:' + self.token_id + '\n' + \
                'chainType:' + self.chain_type + '\n' + \
                'chainID:' + self.chain_id + '\n' + \
                'data:' + self.data + '\n' + \
                'version:' + self.version 

    def get_ever_hash(self):
        message = encode_defunct(text=str(self))
        message_hash = _hash_eip191_message(message)
        return w3.to_hex(message_hash)

    def to_dict(self):
        return {
            'tx_id': self.tx_id,
            'tokenSymbol': self.token_symbol,
            'action': self.action,
            'from': self.from_,
            'to': self.to,
            'amount': self.amount,
            'fee': self.fee,
            'feeRecipient': self.fee_recipient,
            'nonce': self.nonce,
            'tokenID': self.token_id,
            'chainType': self.chain_type,
            'chainID': self.chain_id,
            'data': self.data,
            'version': self.version,
            'sig': self.sig
        }

    def post(self, api_host):
        url = api_host + '/tx'
        if not self.sig:
            raise Exception(self.tx_id, 'no signature.')
        #print('post_data:', self.to_dict())
        return requests.post(url, json=self.to_dict())
