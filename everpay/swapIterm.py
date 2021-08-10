import json


class SwapItem:
    def __init__(self, tag, chain_id, from_, to, amount):
        self.tag = tag
        self.chain_id = chain_id
        self.from_ = from_
        self.to = to
        self.amount = amount

    def getter(self):
        return {
            "tag": self.tag,
            "chainID": self.chain_id,
            "from": self.from_,
            "to": self.to,
            "amount": self.amount
        }
