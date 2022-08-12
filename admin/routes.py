from flask import Blueprint, request, Response, url_for, render_template, send_from_directory, redirect
from utils.sessions import verifyAdminSession, createAdminSession, deleteAdminSession
from settings import getSetting
import requests

admin = Blueprint("admin", __name__)

@admin.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        sid = request.cookies.get("SID")
        if not sid or not verifyAdminSession(sid): return render_template("login.html", msg="")
        else: return render_template("index.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not username or not password: return render_template("login.html", msg="Please fill in all fields")
        if username != str(getSetting("adminUsername")) or password != str(getSetting("adminPassword")):  return render_template("login.html", msg="Invalid username or password")
        session = createAdminSession(username, password)
        resp = redirect(url_for("admin.index"))
        resp.set_cookie("SID", session)
        return resp

@admin.route("/connections", methods=["GET"])
def connections():
    sid = request.cookies.get("SID")
    if not sid or not verifyAdminSession(sid): return render_template("login.html", msg="")
    else: return render_template("connections.html")

@admin.route("/channels", methods=["GET"])
def channels_():
    sid = request.cookies.get("SID")
    baseURL = request.base_url.split("/admin")[0]
    if not sid or not verifyAdminSession(sid): return render_template("login.html", msg="")
    else: return render_template("channels.html", channels=requests.get(f"{baseURL}/api/channels", cookies={'SID': sid}).json())

@admin.route("/users", methods=["GET"])
def users():
    sid = request.cookies.get("SID")
    baseURL = request.base_url.split("/admin")[0]
    if not sid or not verifyAdminSession(sid): return render_template("login.html", msg="")
    else: return render_template("users.html", users=requests.get(f"{baseURL}/api/users", cookies={'SID': sid}).json())

@admin.route("/logout", methods=["GET"])
def logout():
    sid = request.cookies.get("SID")
    if not sid: return Response(status=302)
    deleteAdminSession(sid)
    resp = Response(status=302)
    resp.set_cookie("SID", "", expires=0)
    return resp

@admin.route('/static/<path:path>')
def static_file(path):
    return send_from_directory('static', path)
