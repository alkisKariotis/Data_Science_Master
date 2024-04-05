# ----- ----- ----- Kafka Consumer 0 - Sending Blocks to MongoDB ----- ----- -----

# Import Libraries
from kafka import KafkaConsumer
from pymongo import MongoClient
import json

# Configure Kafka Consumer for partition 0
consumer = KafkaConsumer(
    'Blocks',                                       # Topic
    bootstrap_servers=['localhost:9092'],           # Kafka Bootstrap Servers
    auto_offset_reset='earliest',                   # Start Reading at the Earliest Message
    enable_auto_commit=True,                        # Automatically Commit Offsets
    group_id='block-consumer-group-0',              # Consumer Group ID
    value_deserializer=lambda x: x.decode('utf-8')  # Deserialize Message Value as UTF-8 string
)

# Configure MongoDB
client = MongoClient('localhost', 27017)
db = client['database_itc6107']
collection = db['blocks']

# Listen for Messages & Store Mined Blocks to MongoDB
for message in consumer:
    block_data = json.loads(message.value)
    if block_data['sequence_number'] % 2 == 0:      # Reads only blocks from partition 0 (Even Sequence Number)
        collection.insert_one(block_data)
        print(f"Block Read & Written to MongoDB: {block_data}")
