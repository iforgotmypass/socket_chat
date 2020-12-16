import datetime
import socket
from threading import Thread


class serverApp():
    def __init__(self, host, port):
        self.clients = {}
        self.addresses = {}
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((host, port))
        self.s.listen(3)
        self.printmsg("Started the server.")

    def getTime(self):
        return datetime.datetime.now().strftime("%H:%M:%S")

    def send(self, client, msg):
        client.send(bytes(msg, 'utf-8'))

    def printmsg(self, msg, client='SERVER'):
        try:
            print(f'\r[{self.getTime()}] {client}: {msg}')
        except:
            print("ERROR")


    def sendToAll(self, msg):
        for client in self.clients:
            self.send(client, msg)
            # self.printmsg(client, msg)

    def connectionHandler(self):
        while True:
            client, address = self.s.accept()
            self.send(client, "Hello, type your nickname (max 20 characters): ")
            self.printmsg("Connected", 'Stranger')
            self.addresses[client] = address
            Thread(target=self.clientHandler, args=(client,)).start()

    def clientHandler(self, client):
        nickname = client.recv(20).decode('utf-8')
        self.send(client, f"You've joined the chat, {nickname}")
        self.printmsg(f"{nickname} joined the chat")
        self.sendToAll(f'[{self.getTime()}] SERVER: {nickname} joined the chat.')
        self.clients[client] = nickname

        while True:
            try:
                message = client.recv(50)
                if message == '/quit':
                    client.close()
                    del self.clients[client]
                    break
                self.printmsg(message.decode('utf-8'), nickname)
                self.sendToAll(f'[{self.getTime()}] {nickname}: {message.decode("utf-8")}')
            except:
                print("Error!")
                break

