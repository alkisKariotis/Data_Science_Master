# ----- ----- ----- Blockchain Mining & Writing to Kafka Topic ----- ----- -----

# Import Libraries
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import json
import hashlib
import time
from kafka import KafkaProducer

# Global variable to store the blockchain
blockchain = []

def mine_block(transactions, producer):
    global blockchain

    # Start timing the mining process
    start_time = time.time()

    if not blockchain:  # If blockchain is empty, add the genesis block
        genesis_block = {
            'sequence_number': 0,
            'transactions': 'Genesis block',
            'nonce': 0,
            'prev_hash': '0'  # Previous Block's Hash = '0'
        }
        blockchain.append(genesis_block)
        prev_hash = '0'
    else:
        prev_hash = blockchain[-1]['hash']

    block = {
        'sequence_number': len(blockchain),
        'transactions': transactions,
        'nonce': 0,  # Initialize nonce as an integer
        'prev_hash': prev_hash
    }

    # Proof of Work Algorithm Setup
    difficulty_prefic = '000'  # Target Hash Prefix
    while True:
        block_string = json.dumps(block, sort_keys=True)
        block_hash = hashlib.sha256(block_string.encode()).hexdigest()
        if block_hash.startswith(difficulty_prefic):
            break  # Correct Nonce Found
        else:
            block['nonce'] += 1  # Increment Nonce
            block['nonce'] %= 2**32  # Ensure Nonce wraps around at 32-bit limit

    # Block Hash
    block['hash'] = block_hash

    # End Time of Block Mining Process
    end_time = time.time()
    block['mine_time'] = round((end_time - start_time), 3)

    # Append Mined Block to the Blockchain
    blockchain.append(block)

    # Print Block Details
    print(f'Block Sequence Number: {block['sequence_number']}')
    print(f'Number of Transactions: {len(block['transactions'])}')
    print(f'Block's Nonce: {block['nonce']}')
    print(f'Block’s Digest (Hash): {block['hash']}')
    print(f'Time to Mine: {block['mine_time']} seconds')
    
    # Print Blockchain
    print_blockchain()

    # Sending Block to Kafka
    if block['sequence_number'] % 2 == 0:
        # Send Block to Partition 0 (Even Sequence Numbers)
        producer.send('Blocks', key=b'even', value=json.dumps(block).encode('utf-8'))
    else:
        # Send Block to Partition 1 (Odd Sequence Numbers)
        producer.send('Blocks', key=b'odd', value=json.dumps(block).encode('utf-8'))

def print_blockchain():
    global blockchain
    print('Blockchain:')
    for block in blockchain:
        print(block)
    print()

def create_kafka_producer():
    return KafkaProducer(bootstrap_servers='localhost:9092')

def create_kafka_topic():
    admin_client = KafkaAdminClient(bootstrap_servers='localhost:9092')
    topic = NewTopic(name="Blocks", num_partitions=2, replication_factor=1)
    try:
        admin_client.create_topics([topic])
    except TopicAlreadyExistsError:
        print('Topic 'Blocks' already exists.')

def main():
    # Create Kafka topic with two partitions
    create_kafka_topic()

    sc = SparkContext(appName='BlockchainMining')

    # Get the number of cores available
    num_cores = sc.defaultParallelism

    ssc = StreamingContext(sc, 120)  # 2-minute interval

    # Create a DStream that connects to the server
    dstream = ssc.socketTextStream('localhost', 9999)

    # Initialize Kafka producer
    kafka_producer = create_kafka_producer()

    # Process transactions and mine blocks
    dstream.foreachRDD(lambda rdd: mine_block(rdd.collect(), kafka_producer))

    ssc.start()  # Start the computation
    ssc.awaitTermination()  # Wait for the computation to terminate

if __name__ == '__main__':
    main()
