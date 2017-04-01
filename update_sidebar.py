import os
import re
import time, threading

import praw

import twitch
import gosu

r = None
subname = "dota2test"

def login():
    global r

    r = praw.Reddit(client_id=os.environ["CLIENT_ID"],
                         client_secret=os.environ["CLIENT_SECRET"],
                         password=os.environ["BOT_PASSWORD"],
                         user_agent='Dota 2 sidebar bot',
                         username=os.environ["BOT_USERNAME"])

def update_streamers(sidebar_contents):
    header = "[*Livestreams*](#heading)"
    footer = "**[More Live Streams]" 

    header_index = sidebar_contents.index(header) + len(header) + 4
    footer_index = sidebar_contents.index(footer)

    new_sidebar = sidebar_contents[:header_index] + twitch.get_top_channels() + sidebar_contents[footer_index:]

    return new_sidebar

def update_matches(sidebar_contents):
    header = "[*Upcoming Matches*](#heading)"
    footer = "**[More Upcoming]" 

    header_index = sidebar_contents.index(header) + len(header) + 4
    footer_index = sidebar_contents.index(footer)

    new_sidebar = sidebar_contents[:header_index] + gosu.get_matches() + sidebar_contents[footer_index:]

    return new_sidebar

def get_sidebar():
    sub = r.subreddit(subname)
    mod = sub.mod
    settings = mod.settings()
    sidebar_contents = settings['description']
    
    return sidebar_contents

def push_sidebar(new_sidebar):
    sub = r.subreddit(subname)
    mod = sub.mod
    settings = mod.settings()

    fullname = settings.pop('subreddit_id')

    remap = {'allow_top': 'default_set',
                 'lang': 'language',
                 'link_type': 'content_options'}

    for (new, old) in remap.items():
        settings[new] = settings.pop(old)

    settings.update({"description": new_sidebar})

    sub._create_or_update(_reddit=sub._reddit, sr=fullname, **settings)

def do_update_sidebar(sidebar):
    sidebar = update_streamers(sidebar)
    sidebar = update_matches(sidebar)

    return sidebar

def update_sidebar():
    print time.ctime()
    print "UPDATING!"

    sidebar = get_sidebar()
    sidebar = do_update_sidebar(sidebar)
    push_sidebar(sidebar)

    threading.Timer(30, update_sidebar).start()

if __name__ == "__main__":
    login()
    update_sidebar()
