from block import Block
from blockchain import Blockchain
from transaction import Transaction
from wallet import Wallet

blockchain = Blockchain()

wallet = Wallet()

for i in range(4):
  block = blockchain.generate_next_block()
  block.add_coinbase_transaction(wallet.public_key, blockchain.block_reward)
  block.transactions.append(Transaction(wallet.public_key, wallet.private_key, "person", 10))
  block.mine()
  blockchain.add_block(block)


print(blockchain)
