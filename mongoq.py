# ----- ----- ----- Query Mongo DB ----- ----- -----

# Import Libraries
from pymongo import MongoClient

# Configure MongoDB
client = MongoClient('localhost', 27017)
db = client['database_itc6107']
collection = db['blocks']


# ------------------ Question 1 ------------------
# Request User Input for Block's Sequence Number
sequence_number = int(input('Enter the block's sequence number: '))

# Collect Block Information
block = collection.find_one({'sequence_number': sequence_number})

if block:
    block_info = {}
    if 'nonce' in block:
        block_info['nonce'] = block['nonce']
    if 'hash' in block:
        block_info['hash'] = block['hash']
    if 'transactions' in block:
        block_info['transactions_count'] = len(block['transactions'])
    print(f'1. Block Information for block with sequence number {sequence_number}:')
    print(block_info)
else:
    print('Block not found.')
    
# ------------------ Question 2 -------------------
# Smallest Mining Time Block

block = collection.find_one(sort=[('mine_time', 1)])

print('---------------------------------------------------\n')
print('2. Block with the smallest mining time:')
print(block)

# ------------------ Question 3 ------------------
# Average & Cumulative Mining Time for all Mined Blocks

cum_mine_time = 0
blocks_count = 0

for block in collection.find():
    if 'mine_time' in block:
        cum_mine_time += block['mine_time']
        blocks_count += 1
        
if blocks_count > 0:
    avg_mine_time = cum_mine_time / blocks_count
else:
    avg_mine_time = 0

print('---------------------------------------------------\n')
print('3. Average & Cumulative Mine Time for all blocks:')
print({
    'Average Mine Time': avg_mine_time,
    'Cumulative Mine Time of all blocks': cum_mine_time
})

# ------------------ Question 4 ------------------
# Block(s) with the Largest Number of Transactions
print('---------------------------------------------------\n')
print('4. Block(s) with max number of transactions:')

max_transactions = collection.aggregate([
    {'$project': {'transactions_count': {'$size': '$transactions'}}},
    {'$group': {'_id': None,'max_transactions': {'$max': '$transactions_count'}}}
])
max_transactions_count = max_transactions.next()['max_transactions']

blocks = collection.find({'transactions': {'$size': max_transactions_count}})
max_transactions_blocks = list(blocks)

# Prints the Sequence Number of the Block(s) with max Transactions
print("Sequence number(s) of block(s) with max number of transactions: " +
      ", ".join(str(x['sequence_number']) for x in max_transactions_blocks))
      
# Prints the contents of the Block or Blocks with max Transactions       
# print(max_transactions_blocks) # commented out to avoid repetition

# Prints max number of transactions found in a Block or Blocks
print("Maximum Number of Transactions in block(s):", max_transactions_count) 

# Prints Number of Block(s) with max Transactions
print("Number of block(s) with largest Number of Transactions:", len(max_transactions_blocks))