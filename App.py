import datetime
import socket
from sys import stdout
from threading import Thread
from users import *


class App():
    def __init__(self, isServer = False, host='', port=0):
        self.cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if isServer:
            with open('userdata.json', 'r') as f:
                self.operators = json.load(f)['users']['operators']
            self.clients = {}
            self.addresses = {}
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.bind((host, port))
            self.s.listen(3)
            self.printmsgServer("Started the server.")

    def connect(self, ip, port):
        try:
            self.cs.connect((ip,port))
            print(f'[{self.getTime()}] Connected to server: {ip}:{port}')
        except:
            print("Failed to connect to server.")

    def getTime(self):
        return datetime.datetime.now().strftime("%H:%M:%S")

    def send(self, msg):
        self.cs.send(bytes(msg, 'utf-8'))

    def sendServer(self, client, msg):
        client.send(bytes(msg, 'utf-8'))

    def printmsgServer(self, msg, client='SERVER'):
        try:
            print(f'\r[{self.getTime()}] {client}: {msg}\n', end='')
        except:
            pass

    def printmsg(self, msg):
        try:
            print(f'\r{msg.decode("utf-8")}\nMessage: ', end='')
        except:
            pass

    def sendToAll(self, msg):
        for user in self.clients.values():
            self.sendServer(user.user, msg)

    def serverConnectionHandler(self):
        while True:
            client, address = self.s.accept()
            with open('userdata.json', 'r') as userdata:
                banned = json.load(userdata)['users']['banned']
            if address[0] in banned:
                self.sendServer(client, 'You are banned from this server.')
                continue
            else:
                self.sendServer(client, "Hello, type your nickname (max 20 characters): ")
                self.printmsgServer("Connected", 'Stranger')
                self.addresses[client] = address
            Thread(target=self.clientHandler, args=(client, address,)).start()

    def clientHandler(self, client, address):
        nickname = client.recv(20).decode('utf-8')
        self.sendServer(client, f"You've joined the chat, {nickname}")
        self.printmsgServer(f"{nickname} joined the chat\n")
        self.sendToAll(f'[{self.getTime()}] SERVER: {nickname} joined the chat.')
        self.clients[nickname] = User(nickname, address, client)

        while True:
            try:
                message = client.recv(50)
                decodedMsg = message.decode('utf-8')
                if decodedMsg[0] == '/':
                    print('szukam')
                    if message == '/quit':
                        client.close()
                        self.sendToAll(f'[{self.getTime()}] {nickname} disconnected. (error)')
                        del self.clients[client]
                        break
                    if nickname in self.operators:
                        tmpUser = re.findall('/\w+ (\w+)', decodedMsg)[0]
                        print(tmpUser)
                        if '/op' in decodedMsg:
                            self.clients[tmpUser].op()
                            self.sendToAll(f'{tmpUser} opped.')
                            self.printmsgServer(f'{tmpUser} opped.')
                        elif '/deop' in decodedMsg:
                            self.clients[tmpUser].deop()
                            self.sendToAll(f'{tmpUser} deopped.')
                            self.printmsgServer(f'{tmpUser} deopped.')
                        elif '/ban' in decodedMsg:
                            self.clients[tmpUser].ban()
                            self.sendToAll(f'{tmpUser} banned.')
                            self.printmsgServer(f'{tmpUser} banned.')
                        elif '/unban' in decodedMsg:
                            self.clients[tmpUser].unban()
                            self.sendToAll(f'{tmpUser} unbanned.')
                            self.printmsgServer(f'{tmpUser} unbanned.')
                        elif '/kick' in decodedMsg:
                            pass
                else:
                    self.printmsgServer(decodedMsg, nickname)
                    self.sendToAll(f'[{self.getTime()}] {nickname}: {message.decode("utf-8")}')
            except socket.error:
                del self.clients[nickname]
                self.printmsgServer(f'{nickname} disconnected. (error)')
                self.sendToAll(f'[{self.getTime()}] {nickname} disconnected. (error)')
                break


    def clientConnectionHandler(self):
        Thread(target=self.incomingMessagesHandler).start()
        Thread(target=self.sendingMessagesHandler).start()


    def incomingMessagesHandler(self):
        while True:
            try:
                message = self.cs.recv(50)
                self.printmsg(message)
            except:
                print("Error!")
                break

    def sendingMessagesHandler(self):
        while True:
            messageToSend = input("Message: ")
            if messageToSend == '/quit':
                self.printmsg('Disconnected.')
                break
            elif messageToSend == '':
                stdout.write("\033[F")
                stdout.write('\rMessage cannot be empty.\n')
                print("\033[<10>C")
            else:
                self.send(messageToSend)
                stdout.write("\033[F")
                self.printmsg(messageToSend)