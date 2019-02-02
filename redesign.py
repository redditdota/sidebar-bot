import praw
import twitch


def update_sidebar(sub):
    for w in sub.widgets.sidebar:
        if isinstance(w, praw.models.TextArea):
            if "Livestreams" in w.shortName:
                # do something
                print(w.text)
            elif "Upcoming Matches" in w.shortName:
                # do something else
                print(w.text)

