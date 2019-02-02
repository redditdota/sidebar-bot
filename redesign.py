import praw
import twitch
import gosu

MAX_LENGTH = 20

ABBREVIATIONS = {
    "Season " : "S",
    "Qualifier" : "Qual"
}

def get_top_channels(sub):
    text = "Twitch | 👁 | Streamer \n"
    text += ":- | :- | :- \n"

    channels = twitch.get_top_channels_raw(sub)
    if len(channels) == 0:
        return ""

    for channel in channels:
        status = channel["status"]
        if "|" in status:
            status = status[:status.index("|")]
        if len(status) > MAX_LENGTH:
            status = status[:MAX_LENGTH] + "..."

        text += "[%s](%s) |" % (status, channel["url"])
        text += " %d | " % (channel["viewers"])
        text += "[%s](%s) \n " % (channel["name"], channel["url"])
    return text


def shorten(tournament):
    for word in ABBREVIATIONS.keys():
        if word in tournament:
            tournament = tournament.replace(word, ABBREVIATIONS[word])
    return tournament


def get_matches():
    text = "Time | Team | vs | Team | Tournament\n"
    text += ":- | :-: | :- | :-: | :- \n"

    matches = gosu.get_gosu_matches()
    if len(matches) == 0:
        return ""

    for match in matches:
        text += "[%s](%s)" % (match["time"], match["link"]) + " | "
        text += match["team1"] + " | "
        text += "vs" + " | "
        text += match["team2"] + " | "
        text += shorten(match["tournament"]) + "\n"

    return text


def update_sidebar(sub):
    for w in sub.widgets.sidebar:
        if isinstance(w, praw.models.TextArea):
            if "Livestreams" in w.shortName:
                text = get_top_channels(sub)
                if len(text) > 0:
                    w.mod.update(text=text)
            elif "Upcoming Matches" in w.shortName:
                text = get_matches()
                if len(text) > 0:
                    w.mod.update(text=text)

