# ----- ----- ----- Set Up Server & Generate Transactions ----- ----- -----

# Import Libraries
import socket
import time

# Establish TCP/IP Connection
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define Server Address & Port
host = 'localhost'
port = 9999
server_address = (host, port)

print('Starting server on {}:{}'.format(host, port))

try:
    # Bind the Socket to the Port
    server_socket.bind(server_address)

    # Listen for Incoming Connections
    server_socket.listen(1)

    while True:
        print('Waiting for a connection...')
        connection, client_address = server_socket.accept()
        print('Connection from', client_address)

        try:
            counter = 0
            while True:
                # Generate Transactions
                transaction_string = "Transaction_" + str(counter)
                print(transaction_string)
                counter += 1

                # Encode & Send Transactions
                connection.sendall((transaction_string + "\n").encode())

                # 1 second Waiting Time
                time.sleep(1)
        finally:
            # Close the Connection
            connection.close()
finally:
    # Close the Server Socket
    server_socket.close()
