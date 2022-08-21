from flask import Flask, request, Response, url_for, send_from_directory
from utils.sessions import createSession, verifySession, findAllExpired
from utils.channels import getDisabledChannels
from utils.users import login
from utils.common import getIP, fakeHeaders
from api.routes import api
from admin.routes import admin
from settings import getSetting
import requests
import base64
import json
import re

app = Flask(__name__)
findAllExpired()
proxy = "143.244.45.5:3128"
protocol = "http"


proxies = {
    "http": f"{protocol}://{proxy}",
    "https": f"{protocol}://{proxy}"
}


def disabledVideo():
    return open("static/video/disabled.m3u8", "r").read()

@app.route("/")
def index():
    return "Reborn"

@app.route("/<username>/<password>/playlist.m3u")
def playlistm3u(username, password):
    if not login(username, password): return Response("Forbidden", status=403)
    channelInfo = requests.get(str(getSetting("channelInfo"))).text.split("\n")
    disabledChannels = getDisabledChannels()
    m3u = "#EXTM3U\n"
    for line in channelInfo:
        if line == "": continue
        line = line.split(" | ")
        name = line[0]
        id = line[1]
        logo = line[2]
        vpn = True
        try: vpn = line[4]
        except: vpn = False
        if vpn and getSetting("vpn").lower() != "true": continue
        url = url_for("play", username=username, password=password, channel=id, _external=True)
        if id in disabledChannels: continue
        m3u += f'#EXTINF:-1 tvg-id="{id}" tvg-logo="{logo}",{name}\n{url}\n'
    return Response(m3u, mimetype="text/plain")

@app.route('/<username>/<password>/<channel>.m3u8')
def play(username, password, channel):
    findAllExpired()
    token = createSession(username, password, channel, getIP(request))
    if not token: return Response("Forbidden", status=403)
    if channel in getDisabledChannels(): return disabledVideo()
    resp = requests.get(f"https://ustvgo.tv/player.php?stream={channel}", headers=fakeHeaders, proxies=proxies).text
    resp = resp.replace('\n', '')
    playlistURL = resp.split("hls_src='")[1].split("'")[0]
    chunksURL = playlistURL.split("playlist")[0] + requests.get(playlistURL, headers=fakeHeaders, proxies=proxies).text.split("\n")[3]
    token["url"] = chunksURL
    token = base64.b64encode(json.dumps(token).encode('utf-8')).decode('utf-8')
    return f'#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-STREAM-INF:BANDWIDTH=880723,RESOLUTION=640x360,CODECS="avc1.64001e,mp4a.40.2"\n{url_for("playlistm3u8", token=token, _external=True)}'

@app.route('/playlist.m3u8')
def playlistm3u8():
    token = request.args.get("token")
    baseURL = request.base_url.split("/playlist.m3u8")[0]
    if not token: return Response("Forbidden", status=403)
    token = json.loads(base64.b64decode(token).decode('utf-8'))
    if not verifySession(token["session"], token["username"], token["password"], token["channel"]): return Response("Forbidden", status=403)
    resp = requests.get(token["url"], headers=fakeHeaders, proxies=proxies).text
    baseURL = token["url"].split("chunks.m3u8")[0]
    token["baseURL"] = baseURL
    links = [f"{baseURL}l_{link}" for link in re.findall(r'l_([^\n]+)', resp)]
    for link in links:
        ts = "l_" + link.split("/l_")[1].split(".")[0]
        token["args"] = link.split("?")[1]
        resp = resp.replace(
            link.replace(baseURL, ""),
            url_for("ts", item=ts, token=base64.b64encode(json.dumps(token).encode('utf-8')).decode('utf-8'), _external=True)
        )
    return resp

@app.route('/<item>.ts')
def ts(item):
    token = request.args.get("token")
    if not token: return Response("Forbidden", status=403)
    token = json.loads(base64.b64decode(token).decode('utf-8'))
    if not verifySession(token["session"], token["username"], token["password"], token["channel"]): return Response("Forbidden", status=403)
    return requests.get(token['baseURL'] + item + ".ts?" + token['args'], headers=fakeHeaders, proxies=proxies).content

@app.route('/static/<path:path>')
def static_file(path):
    return send_from_directory('static', path)

app.config['JSON_SORT_KEYS'] = False
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(admin, url_prefix='/admin')
app.run(host=str(getSetting("ip")), port=int(getSetting("port")), debug=getSetting("debug").lower() == "true")