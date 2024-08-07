from time import time
from hashlib import sha256
from random import getrandbits
from transaction import Transaction


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
  def hash(self) -> str:
    block_string = f"{self.prev_hash}{self.nonce}{self.timestamp}{self.height}"

    for transaction in self.transactions:
      block_string += transaction.as_string

    encoded_block_string = block_string.encode()
    return sha256(encoded_block_string).hexdigest()
  
  def add_coinbase_transaction(self, miner: str, reward: float):
    if len(self.transactions) == 0:
      self.transactions.append(Transaction.coinbase(miner, reward))

  def mine(self):
    while self.hash > self.target:
      self.nonce = format(getrandbits(64), "x")
      self.timestamp = time()

    print(f"Mined block #{self.height}")
  
  def verify_transaction_signatures(self) -> bool:
    if len(self.transactions) == 0:
      return False

    if self.transactions[0].type != 'coinbase':
      return False

    for transaction in self.transactions[1:]:
      if transaction.type == 'coinbase' or not transaction.verify():
        return False

    return True
  
  def verify_block_reward(self, block_reward: float) -> bool:
    if not self.transactions or self.transactions[0].sender != 'coinbase':
      return False
    
    if self.transactions[0].amount != block_reward:
      return False

    return True    
