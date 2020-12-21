from App import *
from threading import Thread

# DEFINE IP AND PORT OF YOUR SERVER
IP = '192.168.0.150'
PORT = 2137

# CONNECTING TO SERVER
client = App()
client.connect(IP, PORT)

# STARTING RECEIVING AND SENDING MESSAGES
client.incomingMessagesHandler()