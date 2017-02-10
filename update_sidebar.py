import re
import time, threading

import praw

import twitch

r = None

def login():
    global r

    r = praw.Reddit(client_id='hnexQa51gEfhzg',
                         client_secret='wE5-dMBrclX0N99i7ANY35sqUYM',
                         password='',
                         user_agent='Dota 2 sidebar bot',
                         username='VRCbot')
def update_streamers():
    sub = r.subreddit("dota2test")
    mod = sub.mod
    settings = mod.settings()
    sidebar_contents = settings['description']

    print settings

    header = "[*Livestreams*](#heading)"
    footer = "**[More Live Streams]" 

    header_index = sidebar_contents.index(header) + len(header) + 4
    footer_index = sidebar_contents.index(footer)

    #print sidebar_contents[header_index:footer_index]

    new_sidebar = sidebar_contents[:header_index] + twitch.get_top_channels() + sidebar_contents[footer_index:]

    #print new_sidebar

    fullname = settings.pop('subreddit_id')

    remap = {'allow_top': 'default_set',
                 'lang': 'language',
                 'link_type': 'content_options'}
    for (new, old) in remap.items():
        settings[new] = settings.pop(old)

    settings.update({"description": new_sidebar})

    sub._create_or_update(_reddit=sub._reddit, sr=fullname, **settings)

def update_matches():
    pass

def update_sidebar():
    print time.ctime()
    print "UPDATING!"

    update_streamers()

    threading.Timer(30, update_sidebar).start()

login()
update_sidebar()
