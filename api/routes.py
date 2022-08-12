from flask import Blueprint, send_file, url_for, redirect, Response, request, jsonify
from utils.sessions import verifyAdminSession, deleteSession
from utils.users import addUser, removeUser, resetPassword, getUsers
from utils.channels import getDisabledChannels, disableChannel, enableChannel
from utils.paths import DB_FOLDER
from settings import getSetting
import requests
import os

api = Blueprint("api", __name__)

@api.route("/activeConnections", methods=["GET"])
def activeConnections():
    return send_file(os.path.join(DB_FOLDER, "sessions.json"))

@api.route('/closeConnection/<session>', methods=["GET"])
@api.route('/closeConnection/', methods=["GET"], defaults={"session": None})
def closeConnection(session):
    if not session: return Response("Forbidden", status=403)
    sid = request.cookies.get("SID")
    if not sid or not verifyAdminSession(sid): return Response("Forbidden", status=403)
    deleteSession(session)
    return redirect(url_for("admin.connections"))

@api.route('/createUser/<username>/<password>', methods=["GET"])
def createUser_(username, password):
    if not username or not password: return Response("Forbidden", status=403)
    sid = request.cookies.get("SID")
    if not sid or not verifyAdminSession(sid): return Response("Forbidden", status=403)
    addUser(username, password)
    return Response("OK", status=200)

@api.route('/deleteUser/<username>', methods=["GET"])
def deleteUser_(username):
    if not username: return Response("Forbidden", status=403)
    sid = request.cookies.get("SID")
    if not sid or not verifyAdminSession(sid): return Response("Forbidden", status=403)
    removeUser(username)
    return Response("OK", status=200)

@api.route('/users', methods=["GET"])
def users_():
    sid = request.cookies.get("SID")
    if not sid or not verifyAdminSession(sid): return Response("Forbidden", status=403)
    return getUsers()

@api.route('/resetPassword/<username>/<password>', methods=["GET"])
def resetPassword_(username, password):
    if not username or not password: return Response("Forbidden", status=403)
    sid = request.cookies.get("SID")
    if not sid or not verifyAdminSession(sid): return Response("Forbidden", status=403)
    resetPassword(username, password)
    return Response("OK", status=200)

@api.route('/channels', methods=["GET"])
def channels():
    sid = request.cookies.get("SID")
    if not sid or not verifyAdminSession(sid): return Response("Forbidden", status=403)
    response = {}
    disabled = getDisabledChannels()
    channelInfo = requests.get(str(getSetting("channelInfo"))).text.split("\n")
    for line in channelInfo:
        if line == "": continue
        line = line.split(" | ")
        name = line[0]
        id = line[1]
        logo = line[2]
        try:
            if "VPN" in line[4]: vpn = True
        except: vpn = False
        response[id] = {
            "name": name,
            "logo": logo,
            "vpn": vpn,
            "id": id
        }
        if id in disabled: response[id]["disabled"] = True
        else: response[id]["disabled"] = False
    return jsonify(response)

@api.route('/disableChannel/<channel>', methods=["GET"])
def disableChannel_(channel):
    if not channel: return Response("Forbidden", status=403)
    sid = request.cookies.get("SID")
    if not sid or not verifyAdminSession(sid): return Response("Forbidden", status=403)
    disableChannel(channel)
    return Response("OK", status=200)

@api.route('/enableChannel/<channel>', methods=["GET"])
def enableChannel_(channel):
    if not channel: return Response("Forbidden", status=403)
    sid = request.cookies.get("SID")
    if not sid or not verifyAdminSession(sid): return Response("Forbidden", status=403)
    enableChannel(channel)
    return Response("OK", status=200)

@api.route('/disableIfEnabled/<channel>', methods=["GET"])
def disableIfEnabled_(channel):
    if not channel: return Response("Forbidden", status=403)
    sid = request.cookies.get("SID")
    if not sid or not verifyAdminSession(sid): return Response("Forbidden", status=403)
    disabled = getDisabledChannels()
    if channel in disabled: return Response("OK", status=200)
    disableChannel(channel)
    return Response("OK", status=200)

@api.route('/enableIfDisabled/<channel>', methods=["GET"])
def enableIfDisabled_(channel):
    if not channel: return Response("Forbidden", status=403)
    sid = request.cookies.get("SID")
    if not sid or not verifyAdminSession(sid): return Response("Forbidden", status=403)
    disabled = getDisabledChannels()
    if channel not in disabled: return Response("OK", status=200)
    enableChannel(channel)
    return Response("OK", status=200)

@api.route('/getDisabledChannels', methods=["GET"])
def getDisabledChannels_():
    sid = request.cookies.get("SID")
    if not sid or not verifyAdminSession(sid): return Response("Forbidden", status=403)
    disabled = getDisabledChannels()
    resp = ""
    for channel in disabled:
        resp += channel + "\n"
    return resp

@api.route("/disableVPNchannels")
def disableVPNchannels():
    sid = request.cookies.get("SID")
    if not sid or not verifyAdminSession(sid): return Response("Forbidden", status=403)
    channels = requests.get(str(getSetting("channelInfo"))).text.split("\n")
    msg = ""
    for line in channels:
        if line == "": continue
        line = line.split(" | ")
        try:
            if "VPN" in line[4]: disableChannel(line[1]); msg += line[1] + "\n"
        except: pass
    return Response(msg, status=200)

@api.route("/enableVPNchannels")
def enableVPNchannels():
    sid = request.cookies.get("SID")
    if not sid or not verifyAdminSession(sid): return Response("Forbidden", status=403)
    channels = requests.get(str(getSetting("channelInfo"))).text.split("\n")
    msg = ""
    for line in channels:
        if line == "": continue
        line = line.split(" | ")
        try:
            if "VPN" in line[4]: enableChannel(line[1]); msg += line[1] + "\n"
        except: pass
    return Response(msg, status=200)