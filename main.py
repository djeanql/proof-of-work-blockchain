from block import Block
from blockchain import Blockchain
from transaction import Transaction
from wallet import Wallet

blockchain = Blockchain()

wallet = Wallet()

block = blockchain.generate_next_block()
block.add_coinbase_transaction(wallet.public_key, blockchain.block_reward)
block.transactions.append(Transaction(wallet.public_key, wallet.private_key, "person", 10))
block.transactions.append(Transaction(wallet.public_key, wallet.private_key, "person", 30))
block.mine()
blockchain.add_block(block)

block = blockchain.generate_next_block()
block.add_coinbase_transaction(wallet.public_key, blockchain.block_reward)

# overspending
block.transactions.append(Transaction(wallet.public_key, wallet.private_key, "person", 10))
block.transactions.append(Transaction(wallet.public_key, wallet.private_key, "person", 20))
block.transactions.append(Transaction(wallet.public_key, wallet.private_key, "person", 20))
block.transactions.append(Transaction(wallet.public_key, wallet.private_key, "person", 20))


block.mine()
blockchain.add_block(block)

print(blockchain.get_balance(wallet.public_key))


print(blockchain)
