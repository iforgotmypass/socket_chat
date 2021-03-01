from App import *
from threading import Thread

# DEFINE IP AND PORT OF YOUR SERVER
IP = ''
PORT = XXXX

# CONNECTING TO SERVER
client = App()
client.connect(IP, PORT)

# STARTING RECEIVING AND SENDING MESSAGES
client.clientConnectionHandler()
