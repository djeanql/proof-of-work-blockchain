from time import time
from hashlib import sha256
from random import getrandbits


class Block:

  def __init__(self, height, prev_hash):
    self.prev_hash = prev_hash
    self.height = height
    self.nonce = ''
    self.timestamp = time()
    self.target = "ffffffffffffffffffffffff"
    self.transactions = []

  def __str__(self):
    return f"Block #{self.height}, hash: {self.hash[:10]}.., prev_hash: {self.prev_hash[:10]}.., nonce: {self.nonce[:10]}.., timestamp: {self.timestamp}, target: {self.target[:10]}.., transactions: {len(self.transactions)}"

  @property
  def hash(self):
    block_string = f"{self.prev_hash}{self.nonce}{self.timestamp}{self.height}"

    for transaction in self.transactions:
      block_string += transaction.as_string

    encoded_block_string = block_string.encode()
    return sha256(encoded_block_string).hexdigest()

  def mine(self):
    while self.hash > self.target:
      self.nonce = format(getrandbits(64), "x")

    print(f"Mined block #{self.height}")
