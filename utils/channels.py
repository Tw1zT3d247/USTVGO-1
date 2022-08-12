from utils.paths import DB_FOLDER
import json
import os

disabledChannelsFile = os.path.join(DB_FOLDER, "disabledChannels.json")
if not os.path.exists(disabledChannelsFile): json.dump({}, open(disabledChannelsFile, "w"))

def getDisabledChannels():
    dc = json.loads(open(disabledChannelsFile).read())
    return dc

def disableChannel(channel):
    dc = json.loads(open(disabledChannelsFile).read())
    dc[channel] = {"disabled": True}
    json.dump(dc, open(disabledChannelsFile, "w"))

def enableChannel(channel):
    dc = json.loads(open(disabledChannelsFile).read())
    del dc[channel]
    json.dump(dc, open(disabledChannelsFile, "w"))