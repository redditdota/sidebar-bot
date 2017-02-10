import requests

def get_top_channels():
    url = 'https://api.twitch.tv/kraken/streams?game=Dota+2'
    headers = {'Client-ID': 'f4nae99irirbffejowopfuulu9o4kw'}

    r = requests.get(url, headers=headers)

    dota_channels = r.json()
    top_dota_channels = []

    for stream in dota_channels['streams'][:5]:
        channel = stream["channel"]

        viewers = stream["viewers"]
        status = channel["status"]
        lang = channel["language"]
        name = channel["display_name"]
        url = channel["url"]

        sidebar_channels = {"name": name, "status": status, "viewers": viewers, "url": url, "lang": lang}
        top_dota_channels.append(sidebar_channels)

    updated_matches = ""

    for channel in top_dota_channels:
        updated_matches += ">>>#[" + channel["status"] + "](" + channel["url"] + ")\n"
        updated_matches += ">##" + "\n"
        updated_matches += ">###" + str(channel["viewers"]) + " @ " + channel["name"] + "\n"
        updated_matches += "\n" + ">>[](#separator)" + "\n\n"

    return updated_matches
