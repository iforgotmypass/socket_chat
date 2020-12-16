import datetime
import socket
from sys import stdout
from threading import Thread


class clientApp():
    def __init__(self):
        self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, ip, port):
        try:
            self.c.connect((ip,port))
        except:
            print("Failed to connect to server.")

    def getTime(self):
        return datetime.datetime.now().strftime("%H:%M:%S")

    def send(self, msg):
        self.c.send(bytes(msg, 'utf-8'))

    def printmsg(self, msg):
        try:
            print(f'\r{msg.decode("utf-8")}\nMessage: ', end='')
        except:
            pass

    def connectionHandler(self):
        Thread(target=self.sendingMessagesHandler).start()
        Thread(target=self.sendingMessagesHandler).start()

    def incomingMessagesHandler(self):
        while True:
            try:
                message = self.c.recv(50)
                self.printmsg(message)
            except:
                print("Error!")
                break

    def sendingMessagesHandler(self):
        while True:
            messageToSend = input("Message: ")
            self.send(messageToSend)
            stdout.write("\033[F")
            self.printmsg(messageToSend)
            if messageToSend == '/quit':
                print(f'[{self.getTime()}] Disconnected.')
                break