import os
import re
import time, threading
import datetime

import praw
import schedule
import heroku3

import prize_pool
import twitch
import gosu
import events
import stupidquestions

r = None
subname = "dota2"

config = None

def login():
    global r
    global config

    r = praw.Reddit(client_id=os.environ["CLIENT_ID"],
                         client_secret=os.environ["CLIENT_SECRET"],
                         password=os.environ["BOT_PASSWORD"],
                         user_agent='Dota 2 sidebar bot',
                         username=os.environ["BOT_USERNAME"])

    heroku_conn = heroku3.from_key(os.environ["HEROKU_API_KEY"])
    app = heroku_conn.apps()['dota2sidebar']
    config = app.config()


def update_prize_pool(sidebar_contents):
    header = "######"
    footer = "(#side)"

    header_index = sidebar_contents.index(header) + len(header)
    footer_index = sidebar_contents.index(footer)

    new_sidebar = sidebar_contents[:header_index] + prize_pool.get_prize_pool() + sidebar_contents[footer_index:]

    return new_sidebar

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

def update_events(sidebar_contents):
    header = "[*Upcoming Events*](#heading)"
    footer = "**[More Events]" 

    header_index = sidebar_contents.index(header) + len(header) + 4
    footer_index = sidebar_contents.index(footer)

    new_sidebar = sidebar_contents[:header_index] + events.get_upcoming_events() + sidebar_contents[footer_index:]

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

def update_flairs():
    for message in r.inbox.unread():
        if "change my flair text" in message.subject.lower():
            if len(message.body) <= 64:
                cssclass = r.subreddit(subname).flair(redditor=message.author).next()['flair_css_class']
                r.subreddit(subname).flair.set(message.author, message.body, cssclass)

                message.reply("""I've changed your flair text to **""" + message.body + """**! Send me a
                        new message if you want it changed again.""")
                message.mark_read()
            else:
                message.reply("""I wasn't able to change your flair text because what you sent me
                        was longer than 64 characters. If you still want something changed, send me
                        **new** message (don't reply to this one) with something shorter!""")
                message.mark_read()
        else:
            if "username mention" not in message.subject:
                message.reply("""I didn't recognize the subject of your message. If you were wanting
                to change your flair text please send a message with the subject **Change My Flair Text**
                . Thanks!""")
            message.mark_read()

def do_update_sidebar(sidebar):
    #sidebar = update_prize_pool(sidebar)
    sidebar = update_streamers(sidebar)
    sidebar = update_matches(sidebar)
    sidebar = update_events(sidebar)

    return sidebar

def update_sidebar():
    print time.ctime()
    print "UPDATING!"

    sidebar = get_sidebar()
    sidebar = do_update_sidebar(sidebar)
    push_sidebar(sidebar)

    update_flairs()

    #threading.Timer(30, update_sidebar).start()

def create_stupid_questions_thread():
    stupidquestions.createPost(r, subname, config["STUPID_QUESTIONS_ID"])
    config["STUPID_QUESTIONS_ID"] = str(int(config["STUPID_QUESTIONS_ID"]) + 1)

def cleanup_stupid_questions_thread():
    stupidquestions.unstickyPost(r)

if __name__ == "__main__":
    login()

    schedule.every(30).seconds.do(update_sidebar)
    schedule.every().monday.at("0:00").do(create_stupid_questions_thread)
    schedule.every().monday.at("23:59").do(cleanup_stupid_questions_thread)

    while True:
        schedule.run_pending()
        time.sleep(1)