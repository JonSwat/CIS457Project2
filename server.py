'''
Title:       Chat Server
Author:      Jon Swiatkowski
Date:        4/17/2020
Description: This program creates a chat server and listens for connections from clients.
'''
import socket
import select

# Declare constants
PORT = 2000
ADDRESS = "127.0.0.1"

# Create the socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind to the port at the address
server.bind((ADDRESS, PORT))

# Listen for new connections
server.listen()

# List of connected users
users = {}

# List of sockets
sockets = [server]

print(f'Listening for connections at {PORT}:')

# Handles incoming message
def receive(client):

    try:
		
        # Get header containing message length
        messageHeader = client.recv(10)

        # Check if no data was receieved
        if not len(messageHeader):
            return False

        # Convert header to int value
        length = int(messageHeader.decode('utf-8').strip())

        # Return header and data
        return {'header': messageHeader, 'data': client.recv(length)}

    except:
        return False

while True:

    # Wait for activity
    newSockets, _, badSockets = select.select(sockets, [], sockets)

    # Go through active sockets
    for activeSocket in newSockets:

        # Check if socket is a server socket
        if activeSocket == server:

            # Accept new connection
            client, clientAddress = server.accept()

            # Receive client name
            user = receive(client)

            # Add socket to list
            sockets.append(client)

            # Get username and header
            users[client] = user

            print('New connection from {}:{}, username: {}'.format(*clientAddress, user['data'].decode('utf-8')))

        # Else existing socket is sending a message
        else:

            # Receive message
            message = receive(activeSocket)

            # Check if client disconnected
            if message is False:
                print('Connection ended from: {}'.format(users[activeSocket]['data'].decode('utf-8')))

                # Remove from list
                sockets.remove(activeSocket)

                # Remove from list of users
                del users[activeSocket]

                continue

            # Get which user sent the message
            user = users[activeSocket]

            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            # Send message to users
            for client in users:

                # Don't send message to sender
                if client != activeSocket:

                    # Send message to users
                    client.send(user['header'] + user['data'] + message['header'] + message['data'])