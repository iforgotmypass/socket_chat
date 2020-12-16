from serverApp import *

# DEFINE HOST NAME AND PORT OF YOUR SERVER
HOST_NAME = socket.gethostname()
PORT =

# SETTING UP THE SERVER
server = serverApp(HOST_NAME, PORT)
server.connectionHandler()