from settings import getSetting
import random
import time
import json
import os
from utils.paths import DB_FOLDER
from string import  ascii_letters, digits
from utils.users import setUserIP, login

sessionsFile = os.path.join(DB_FOLDER, "sessions.json")
adminSessionsFile = os.path.join(DB_FOLDER, "adminSessions.json")
if not os.path.exists(sessionsFile): json.dump({}, open(sessionsFile, "w"))
if not os.path.exists(adminSessionsFile): json.dump({}, open(adminSessionsFile, "w"))

def genSession():
    return ''.join(random.choice(ascii_letters + digits) for _ in range(32))

def createSession(username, password, channel, ip):
    if not login(username, password): return None
    setUserIP(username, ip)
    print("Creating session for " + username)
    session = genSession()
    token = {
        "session": session,
        "username": username,
        "password": password,
        "channel": channel,
        "ip": ip,
        "expiration": time.time() + 5 * 60 # 5 minutes
    }
    sessionsU = json.load(open(sessionsFile))
    sessionsU[session] = token
    json.dump(sessionsU, open(sessionsFile, "w"))
    return token

def updateExpiration(session):
    print("Updating expiration for " + session)
    sessionsU = json.load(open(sessionsFile))
    sessionsU[session]["expiration"] = time.time() + 5 * 60 # 5 minutes
    json.dump(sessionsU, open(sessionsFile, "w"))

def verifySession(session, username, password, channel):
    if not login(username, password): return None
    print("Verifying session for " + username)
    sessionsU = json.load(open(sessionsFile))
    if session not in sessionsU: return False
    token = sessionsU[session]
    if token["username"] != username or token["password"] != password or token["channel"] != channel: return False
    if time.time() > token["expiration"]: return False
    updateExpiration(session)
    return True

def deleteSession(session):
    print("Deleting session for " + session)
    sessionsU = json.load(open(sessionsFile))
    if session in sessionsU:
        del sessionsU[session]
    json.dump(sessionsU, open(sessionsFile, "w"))

def searchForExpiredSessions():
    print("Searching for expired sessions")
    sessionsU = json.load(open(sessionsFile))
    newSessions = {}
    for session in sessionsU:
        if time.time() < sessionsU[session]["expiration"]:
            newSessions[session] = sessionsU[session]
    json.dump(newSessions, open(sessionsFile, "w"))

def createAdminSession(username, password):
    if username != str(getSetting("adminUsername")) or password != str(getSetting("adminPassword")): return None
    session = genSession()
    token = {
        "session": session,
        "username": username,
        "password": password,
        "expiration": time.time() + 7 * 24 * 60 * 60 # 7 days
    }
    sessionsA = json.load(open(adminSessionsFile))
    sessionsA[session] = token
    json.dump(sessionsA, open(adminSessionsFile, "w"))
    return session

def verifyAdminSession(session):
    sessionsA = json.load(open(adminSessionsFile))
    if session not in sessionsA: return False
    token = sessionsA[session]
    if time.time() > token["expiration"]: return False
    return True

def searchForExpiredAdminSessions():
    sessionsA = json.load(open(adminSessionsFile))
    for session in sessionsA:
        if time.time() > sessionsA[session]["expiration"]:
            del sessionsA[session]
    json.dump(sessionsA, open(adminSessionsFile, "w"))

def deleteAdminSession(session):
    sessionsA = json.load(open(adminSessionsFile))
    if session in sessionsA:
        del sessionsA[session]
    json.dump(sessionsA, open(adminSessionsFile, "w"))

def findAllExpired():
    searchForExpiredSessions()
    searchForExpiredAdminSessions()