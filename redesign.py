import praw
import twitch
import gosu

def get_top_channels():
    text = ". | . | . \n"
    for channel in twitch.get_top_channels_raw():
        text += "[%s](%s) |".format(channel["status"], channel["url"])
        text += "👁 %d | ".format(channel["viewers"])
        text += "@ %s \n ".format(channel["name"])
    return text


def get_matches():
    text = "Time | Team | vs | Team | Tournament\n"
    for match in gosu.get_gosu_matches():
        text += match["time"] + " | "
        text += match["team1"] + " | "
        text += "vs" + " | "
        text += match["team2"] + " | "
        text += match["tournament"] + "\n"

    return text


def update_sidebar(sub):
    for w in sub.widgets.sidebar:
        if isinstance(w, praw.models.TextArea):
            if "Livestreams" in w.shortName:
                w.mod.update(text=get_top_channels())
                #print(w.text)
            elif "Upcoming Matches" in w.shortName:
                w.mod.update(text=get_matches())
                #print(w.text)

