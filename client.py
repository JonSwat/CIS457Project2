'''
Title:       Chat Client
Author:      Jon Swiatkowski
Date:        4/17/2020
Description: This program connects a user to a chat server and uses a GUI to get user input.
'''
import socket
import select
import errno
import emojis
from appJar import gui

# Declare constants
HEADER_LENGTH = 10
PORT = 2000
ADDRESS = "127.0.0.1"

# Make sign-in GUI
signIn = gui()
signIn.addLabel("title", "Chat Client")
signIn.setLabelBg("title", "orange")
signIn.addLabelEntry("Username:")
def press(button):
    if button == "Cancel":
        signIn.stop()
    else:
        user = signIn.getEntry("Username:")
        print("Username: " + user)
        signIn.stop()

signIn.addButtons(["Submit", "Cancel"], press)

# Start sign-in GUI
signIn.go()

user = signIn.getEntry("Username:")

# Create the socket
userSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the provided address and port
userSocket.connect((ADDRESS, PORT))
userSocket.setblocking(False)

# Set username and header then send them
username = user.encode('utf-8')
header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
userSocket.send(header + username)

# Make chat GUI
chat = gui()
chat.setBg("orange")
chat.setSize(500,500)
chat.addScrolledTextArea("t1")
chat.addScrolledTextArea("t2")
chat.setTextArea("t1", "Received Messages:")
chat.addLabel("instructions", "-> Enter Messages Above Then Press Send Below<-")
def press(press):
    if press == "Exit":
        chat.stop()
    if press == "Send":
        message = chat.getTextArea("t2")
        chat.clearTextArea("t2")
        chat.setTextArea("t1", "\n" + user + ": " + message)
        print(user + ": " + emojis.encode(message))
            # Check if message is empty
        if message:
            # Encode the message then send it
            message = message.encode('utf-8')
            messageHeader = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            userSocket.send(messageHeader + message)
    else:
            try:
                while True:

                    # Receive header
                    header = userSocket.recv(HEADER_LENGTH)

                    # Check if there is data present
                    if not len(header):
                        print('Server closed connection...')
                        sys.exit()

                    # Convert header to int value
                    userLength = int(header.decode('utf-8').strip())

                    # Receive and decode username
                    username = userSocket.recv(userLength).decode('utf-8')

                    # Receive and decode message
                    messageHeader = userSocket.recv(HEADER_LENGTH)
                    messageLength = int(messageHeader.decode('utf-8').strip())
                    message = userSocket.recv(messageLength).decode('utf-8')

                    # Print message
                    chat.setTextArea("t1","\n" + username + ": " + message)
                    print(username + ": " + emojis.encode(message))

            except IOError as e:

                # Check for exceptions
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Error: {}'.format(str(e)))
                    sys.exit()

chat.addButtons(["Send", "Refresh", "Exit"], press)

# Start chat GUI
chat.go()