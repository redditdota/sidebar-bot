import requests
import os

clientID = os.environ["TWITCH_CLIENT_ID"]

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

def get_top_channels():
    url = 'https://api.twitch.tv/kraken/streams?game=Dota+2'
    headers = {'Client-ID': clientID}

    r = requests.get(url, headers=headers)

    dota_channels = r.json()
    top_dota_channels = []

    counter = 0
    for stream in dota_channels['streams']:
        if counter >= 5:
            break

        channel = stream["channel"]

	if channel["display_name"] in whitelist:
	    pass
        if "dota2ruhub" in channel["display_name"].lower():
            continue
        elif channel["broadcaster_language"] != "en":
            continue

        viewers = stream["viewers"]
        status = channel["status"]
        name = channel["display_name"]
        url = channel["url"]

        sidebar_channels = {"name": name, "status": status, "viewers": viewers, "url": url}
        top_dota_channels.append(sidebar_channels)

        counter += 1

    updated_matches = ""

    for channel in top_dota_channels:
        updated_matches += ">>>#[" + channel["status"] + "](" + channel["url"] + ")\n"
        updated_matches += ">##" + "\n"
        updated_matches += ">###" + str(channel["viewers"]) + " @ " + channel["name"] + "\n"
        updated_matches += "\n" + ">>[](#separator)" + "\n\n"

    return updated_matches
