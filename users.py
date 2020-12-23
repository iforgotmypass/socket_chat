import json
import re

class User:
    def __init__(self, nickname, address, client):
        self.nickname = nickname
        self.user = client
        self.userInfo = address

    def op(self):
        with open('userdata.json', 'r') as userData:
            ops = json.load(userData)
            ops['users']['operators'].append(self.nickname)
        with open('userdata.json', 'w') as f:
            f.write(json.dumps(ops))

    def ban(self):
        with open('userdata.json', 'r') as f:
            userData = json.load(f)
            userData['users']['banned'].append(self.userInfo[0])
        with open('userdata.json', 'w') as f:
            f.write(json.dumps(userData))

    def deop(self):
        with open('userdata.json', 'r') as f:
            userData = json.load(f)
            userData['users']['operators'].remove(self.nickname)
        with open('userdata.json', 'w') as f:
            f.write(json.dumps(userData))

    def unban(self):
        with open('userdata.json', 'r') as f:
            userData = json.load(f)
            userData['users']['banned'].remove(self.userInfo[0])
        with open('userdata.json', 'w') as f:
            f.write(json.dumps(userData))