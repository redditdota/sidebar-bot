from datetime import datetime
import requests
import os
import chess

import configparser

config = configparser.ConfigParser()
config.read("config.txt")

clientID = config.get("config", "TWITCH_CLIENT_ID")

whitelist = ["nooneboss"]

def is_ascii(text):
    if isinstance(text, unicode):
        try:
            text.encode('ascii')
        except UnicodeEncodeError:
            return False
    else:
        try:
            text.decode('ascii')
        except UnicodeDecodeError:
            return False
    return True

def _get_top_channels_raw(url):
    headers = {'Client-ID': clientID}

    r = requests.get(url, headers=headers)

    dota_channels = r.json()
    top_dota_channels = []

    for stream in dota_channels['data']:
        if len(top_dota_channels) >= 5:
            break

        viewers = stream["viewer_count"]
        status = stream["title"]
        name = stream["user_name"]
        url = "https://www.twitch.tv/" + name

        if '`' in status:
            status = status.replace("`", "\`")
        if '[' in status:
            status = status.replace("[", "\[")
        if ']' in status:
            status = status.replace("]", "\]")
        if '\r' in status:
            status = status.replace("\r", '')
        if '\n' in status:
            status = status.replace("\n", '')

        sidebar_channels = {"name": name, "status": status,
                            "viewers": viewers, "url": url}
        top_dota_channels.append(sidebar_channels)

    return top_dota_channels


def _get_top_channels(url):
    updated_matches = ""
    for channel in _get_top_channels_raw(url):
        updated_matches += ">>>#[" + channel["status"] + \
            "](" + channel["url"] + ")\n"
        updated_matches += ">##" + "\n"
        updated_matches += ">###" + \
            str(channel["viewers"]) + " @ " + channel["name"] + "\n"
        updated_matches += "\n" + ">>[](#separator)" + "\n\n"

    return updated_matches

def get_top_artifact_channels():
    return _get_top_channels('https://api.twitch.tv/helix/streams?game_id=16937&language=en')

def get_top_dota_channels():
    return _get_top_channels('https://api.twitch.tv/helix/streams?game_id=29595&language=en')

def get_top_channels_raw(sub):
    if sub.display_name.lower() == "dota2":
        return _get_top_channels_raw('https://api.twitch.tv/helix/streams?game_id=29595&language=en')
    elif sub.display_name.lower() == "artifact":
        return _get_top_channels_raw('https://api.twitch.tv/helix/streams?game_id=16937&language=en')

    return []
