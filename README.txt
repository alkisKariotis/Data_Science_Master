Project: Blockchain with Spark Streaming, Kafka and MongoDB

Overview:
This project implements a simple blockchain system using Apache Kafka for message passing and MongoDB for storing block information. 
It consists of several Python scripts performing different tasks such as generating transactions, mining blocks, processing mined blocks, 
querying block information, and interacting with Kafka and MongoDB.

1. Prerequisites:
   - Spark Streaming: Install and configure Spark Streaming on your system. You can download Spark from the official Apache Spark website: https://spark.apache.org/downloads
   - Apache Kafka: Install and configure Kafka on your system. You can download Kafka from the official Apache Kafka website: https://kafka.apache.org/downloads
   - MongoDB: Install MongoDB on your system. You can download MongoDB from the official MongoDB website: https://www.mongodb.com/try/download/community
   - Python 3.x: Make sure Python 3.x is installed on your system.
   - Docker Desktop: Install Docker Desktop on your system. You can download Docker Desktop from the official website: https://www.docker.com/products/docker-desktop
   - PyCharm: Install PyCharm. You can download PyCharm from the official JetBrains website: https://www.jetbrains.com/pycharm/download/
   
   
2. Open Docker


3. Setting up Kafka in PyCharm Terminal:

	- Check if Kafka Topic exists
    kafka-topics.sh --topic Blocks --describe --bootstrap-server localhost:9092
	
	- Create Kafka Topic
    kafka-topics.sh --create --topic Blocks --replication-factor 1 --partitions 2 --bootstrap-server localhost:9092



4. Setting up MongoDB in PyCharm Terminal:

	- Pull the MongoDB Docker image for MongoDB Community Server version 6.0 based on Ubuntu 22.04
	docker pull mongodb/mongodb-community-server:6.0-ubuntu2204

	- Run a Docker container named 'mongodb' in detached mode (-d) with port forwarding (-p) from host port 27017 to container port 27017
	docker run --name mongodb -d -p 27017:27017 mongodb/mongodb-community-server:6.0-ubuntu2204

	- Database could be create on terminal as below, however we integrated in the py files.
		mongosh mongodb://localhost:27017
		use database_itc6107

5. Add Python Files to Project Folder in PyCharm


6. Open and Run Python Scripts:

   - tr-server.py: Transaction Server
     - This script generates transactions and sends them over a TCP socket.
	 
   - mine.py: Blockchain Miner
     - This script mines blocks using Proof of Work and sends mined block information to a Kafka topic.

   - app0.py: Application to Read Partition 0 of Kafka Topic "Blocks"
     - This script reads partition 0 of the Kafka topic "Blocks" and writes the contents to a MongoDB collection.

   - app1.py: Application to Read Partition 1 of Kafka Topic "Blocks"
     - This script reads partition 1 of the Kafka topic "Blocks" and writes the contents to a MongoDB collection.

   - mongoq.py: MongoDB Query Application
     - This script provides functions to query information from the MongoDB collection "blocks".

7. Important Notes:
   - Ensure Kafka and MongoDB are running before executing the Python scripts.
   - Adjust Kafka and MongoDB configurations as necessary based on your system setup.
   - Make sure to install required Python dependencies (e.g., kafka-python, pymongo) using pip if not already installed.
   - Monitor logs and outputs for any errors or warnings during execution.


