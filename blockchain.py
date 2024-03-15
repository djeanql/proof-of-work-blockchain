from block import Block

from time import time


class Blockchain:

  def __init__(self):
    self.chain = []

  def __str__(self):
    string = f"Blockchain ({len(self.chain)} blocks):\n"
    for block in self.chain:
      string += str(block) + "\n"
    return string

  @property
  def height(self):
    return max(len(self.chain) - 1, 0)

  @property
  def previous_block(self):
    return self.chain[-1] if len(self.chain) > 0 else None

  def add_block(self, block):
    if self.validate_next_block(block):
      self.chain.append(block)
      return True
    else:
      print("Block invalid")
      return False

  def validate_next_block(self, block):

    if block.hash > block.target:
      return False

    if block.timestamp > time():
      return False

    if block.height != 0:

      if block.timestamp < self.previous_block.timestamp:
        return False

      if block.height != self.height + 1:
        return False

      if block.prev_hash != self.previous_block.hash:
        return False

    return True

  def generate_next_block(self):
    return Block(
        self.height +
        1, self.previous_block.hash) if self.previous_block else Block(0, "")
