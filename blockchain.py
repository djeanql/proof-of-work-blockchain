from block import Block
from transaction import Transaction

from time import time


class Blockchain:

  def __init__(self):
    self.chain = []
    self.block_reward = 50.0

  def __str__(self):
    string = f"Blockchain ({len(self.chain)} blocks):\n"
    for block in self.chain:
      string += str(block) + "\n"
    return string

  @property
  def height(self) -> int:
    return max(len(self.chain) - 1, 0)

  @property
  def previous_block(self) -> bool:
    return self.chain[-1] if len(self.chain) > 0 else None

  def add_block(self, block: Block) -> bool:
    if self.validate_next_block(block):
      self.chain.append(block)
      return True
    else:
      print("Block invalid")
      return False

  def validate_next_block(self, block: Block) -> bool:

    if block.hash > block.target:
      return False

    if block.timestamp > time():
      return False
    
    if not block.verify_transaction_signatures():
      return False
    
    if not self.check_for_overspending(block):
      return False

    if not block.verify_block_reward(self.block_reward):
      return False

    if block.height != 0:

      if block.timestamp < self.previous_block.timestamp:
        return False

      if block.height != self.height + 1:
        return False

      if block.prev_hash != self.previous_block.hash:
        return False

    return True
  
  def get_balance(self, wallet_address: str) -> float:
    balance = 0.0
  
    for block in self.chain:
      for transaction in block.transactions:
        if transaction.sender == wallet_address:
          balance -= transaction.amount
        if transaction.recipient == wallet_address:
          balance += transaction.amount
    
    return balance
  
  def check_for_overspending(self, block: Block) -> bool:
    """Checks that no address overspends in a given block"""
    
    balances = {}
  
    for transaction in block.transactions:

      # get current balances
      if transaction.sender not in balances.keys():
        balances[transaction.sender] = self.get_balance(transaction.sender)
      if transaction.recipient not in balances.keys():
        balances[transaction.recipient] = self.get_balance(transaction.recipient)
      
      # edit balances every transaction
      balances[transaction.sender] -= transaction.amount
      balances[transaction.recipient] += transaction.amount

      if transaction.type != 'coinbase' and balances[transaction.sender] < 0:
        return False
    
    return True
  
  def transaction_history(self, wallet_address: str) -> [Transaction]:
    transactions = []
  
    for block in self.chain:
      for transaction in block.transactions:
        if wallet_address in (transaction.sender, transaction.recipient):
          transactions.append(transaction)
    
    return transactions


  def generate_next_block(self):
    return Block(
        self.height +
        1, self.previous_block.hash) if self.previous_block else Block(0, "")
