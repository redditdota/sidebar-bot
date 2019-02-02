import requests
import os

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


def get_top_channels_raw():
    url = 'https://api.twitch.tv/kraken/streams?game=Dota+2'
    headers = {'Client-ID': clientID}

    r = requests.get(url, headers=headers)

    dota_channels = r.json()
    top_dota_channels = []

    for stream in dota_channels['streams']:
        if len(top_dota_channels) >= 5:
            break

        channel = stream["channel"]

        if channel["display_name"] in whitelist:
            pass
        elif "dota2ruhub" in channel["display_name"].lower():
            continue
        elif channel["broadcaster_language"] != "en":
            continue

        viewers = stream["viewers"]
        status = channel["status"]
        name = channel["display_name"]
        url = channel["url"]

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


def get_top_channels():
    updated_matches = ""
    for channel in get_top_channels_raw():
        updated_matches += ">>>#[" + channel["status"] + \
            "](" + channel["url"] + ")\n"
        updated_matches += ">##" + "\n"
        updated_matches += ">###" + \
            str(channel["viewers"]) + " @ " + channel["name"] + "\n"
        updated_matches += "\n" + ">>[](#separator)" + "\n\n"

    return updated_matches

def get_top_artifact_channels():
    url = 'https://api.twitch.tv/kraken/streams?game=Artifact'
    headers = {'Client-ID': clientID}

    r = requests.get(url, headers=headers)

    artifact_channels = r.json()
    top_artifact_channels = []

    for stream in artifact_channels['streams']:
        if len(top_artifact_channels) >= 5:
            break

        channel = stream["channel"]

        if channel["display_name"] in whitelist:
            pass
        elif "dota2ruhub" in channel["display_name"].lower():
            continue
        elif channel["broadcaster_language"] != "en":
            continue

        viewers = stream["viewers"]
        status = channel["status"]
        name = channel["display_name"]
        url = channel["url"]

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
        top_artifact_channels.append(sidebar_channels)

    updated_matches = ""

    for channel in top_dota_channels:
        updated_matches += ">>>#[" + channel["status"] + \
            "](" + channel["url"] + ")\n"
        updated_matches += ">##" + "\n"
        updated_matches += ">###" + \
            str(channel["viewers"]) + " @ " + channel["name"] + "\n"
        updated_matches += "\n" + ">>[](#separator)" + "\n\n"

    return updated_matches
