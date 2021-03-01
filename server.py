from App import *

# DEFINE HOST NAME AND PORT OF YOUR SERVER
HOST_NAME = socket.gethostname()
PORT = XXXX

# SETTING UP THE SERVER
server = App(isServer=True, host=HOST_NAME, port=PORT)
server.serverConnectionHandler()
