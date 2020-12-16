from clientApp import *

# DEFINE IP AND PORT OF YOUR SERVER
IP = ''
PORT =

# CONNECTING TO SERVER
client = clientApp()
client.connect(IP, PORT)
print(f'[{client.getTime()}] Connected: {IP}:{PORT}')

# STARTING RECEIVING AND SENDING MESSAGES
client.connectionHandler()