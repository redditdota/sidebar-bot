import praw
import twitch
import gosu

MAX_LENGTH = 20

ABBREVIATIONS = {
    "Season " : "S",
    "Qualifier" : "Qual"
}

def get_top_channels():
    text = "Twitch | 👁 | Streamer \n"
    text += ":- | :- | :- \n"
    for channel in twitch.get_top_channels_raw():
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
    for match in gosu.get_gosu_matches():
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
                w.mod.update(text=get_top_channels())
                #print(w.text)
            elif "Upcoming Matches" in w.shortName:
                w.mod.update(text=get_matches())
                #print(w.text)

