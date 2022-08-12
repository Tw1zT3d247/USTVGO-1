import os
import json
import hashlib
import random
from utils.paths import DB_FOLDER
from string import ascii_letters, digits

usersFile = os.path.join(DB_FOLDER, "users.json")
if not os.path.exists(usersFile): json.dump({}, open(usersFile, "w"))

def login(username, password):
    users = json.load(open(usersFile))
    if username not in users: return False
    salt = users[username]["salt"]
    if users[username]["hash"] != hashlib.sha256(f"{salt}:{password}".encode()).hexdigest(): return False
    return True

def addUser(username, password):
    users = json.load(open(usersFile))
    salt = ''.join(random.choice(ascii_letters + digits) for _ in range(32))
    users[username] = {
        "salt": salt,
        "hash": hashlib.sha256(f"{salt}:{password}".encode()).hexdigest()
    }
    json.dump(users, open(usersFile, "w"))

def getUsers():
    users = json.load(open(usersFile))
    for user in users:
        del users[user]["hash"]
        del users[user]["salt"]
    return users

def removeUser(username):
    users = json.load(open(usersFile))
    if username in users:
        del users[username]
    json.dump(users, open(usersFile, "w"))

def resetPassword(username, password):
    users = json.load(open(usersFile))
    users[username]["hash"] = hashlib.sha256(f"{users[username]['salt']}:{password}".encode()).hexdigest()
    json.dump(users, open(usersFile, "w"))

def setUserIP(username, ip):
    users = json.load(open(usersFile))
    users[username]["ip"] = ip
    json.dump(users, open(usersFile, "w"))