import os
import re
import sys
import time
import datetime

import praw
import schedule

import prize_pool
import twitch
import gosu
import events
import stupidquestions
import battlecup
import countdown
import redesign
import hero_discussion
import item_discussion

import configparser

config = configparser.ConfigParser()
config.read("config.txt")

r = None
password = None

def login():
    global r
    global password
    global config

    if password is None:
        password = sys.argv[1]
    r = praw.Reddit(
        client_id=config.get("config", "CLIENT_ID"),
        client_secret=config.get("config", "CLIENT_SECRET"),
        password=password,
        user_agent="Dota 2 sidebar bot",
        username=config.get("config", "BOT_USERNAME"),
    )


def update_prize_pool(sidebar_contents):
    header = "######"
    footer = "(#side)"

    if header not in sidebar_contents or footer not in sidebar_contents:
        return sidebar_contents

    if header not in sidebar_contents or footer not in sidebar_contents:
        return sidebar_contents

    header_index = sidebar_contents.index(header) + len(header)
    footer_index = sidebar_contents.index(footer)

    new_sidebar = (
        sidebar_contents[:header_index]
        + prize_pool.get_prize_pool()
        + sidebar_contents[footer_index:]
    )

    return new_sidebar


def update_streamers(sidebar_contents):
    header = "[*Livestreams*](#livestreamheading)"
    footer = "**[More Live Streams]"

    if header not in sidebar_contents or footer not in sidebar_contents:
        return sidebar_contents

    header_index = sidebar_contents.index(header) + len(header) + 4
    footer_index = sidebar_contents.index(footer)

    new_sidebar = (
        sidebar_contents[:header_index]
        + twitch.get_top_dota_channels()
        + sidebar_contents[footer_index:]
    )

    return new_sidebar


def update_artifact_streams(sidebar_contents):
    header = "[*Livestreams*](#welcomeheading)"
    footer = "**[More Live Streams]"

    if header not in sidebar_contents or footer not in sidebar_contents:
        return sidebar_contents

    header_index = sidebar_contents.index(header) + len(header) + 4
    footer_index = sidebar_contents.index(footer)

    new_sidebar = (
        sidebar_contents[:header_index]
        + twitch.get_top_artifact_channels()
        + sidebar_contents[footer_index:]
    )

    return new_sidebar


def update_matches(sidebar_contents):

    header = "[*Upcoming Matches*](#upcomingheading)"
    footer = "**[More Upcoming]"

    if header not in sidebar_contents or footer not in sidebar_contents:
        return sidebar_contents

    header_index = sidebar_contents.index(header) + len(header) + 4
    footer_index = sidebar_contents.index(footer)

    new_sidebar = (
        sidebar_contents[:header_index]
        + gosu.get_matches()
        + sidebar_contents[footer_index:]
    )

    return new_sidebar


def update_events(sidebar_contents):
    header = "[*Upcoming Events*](#upcomingeventsheading)"
    footer = "**[More Events]"

    if header not in sidebar_contents or footer not in sidebar_contents:
        return sidebar_contents

    header_index = sidebar_contents.index(header) + len(header) + 4
    footer_index = sidebar_contents.index(footer)

    new_sidebar = (
        sidebar_contents[:header_index]
        + events.get_upcoming_events()
        + sidebar_contents[footer_index:]
    )

    return new_sidebar


def update_artifact_events(sidebar_contents):
    header = "[*Upcoming Tournaments*](#subsheading)"
    footer = "**[More Tournaments]"

    if header not in sidebar_contents or footer not in sidebar_contents:
        return sidebar_contents

    header_index = sidebar_contents.index(header) + len(header) + 4
    footer_index = sidebar_contents.index(footer)

    new_sidebar = (
        sidebar_contents[:header_index]
        + events.get_upcoming_tournaments()
        + sidebar_contents[footer_index:]
    )

    return new_sidebar


def update_countdown(sidebar_contents):
    header = "######["
    footer = "](#side)"

    if header not in sidebar_contents or footer not in sidebar_contents:
        return sidebar_contents

    header_index = sidebar_contents.index(header) + len(header)
    footer_index = sidebar_contents.index(footer)

    new_sidebar = (
        sidebar_contents[:header_index]
        + countdown.get_countdown()
        + sidebar_contents[footer_index:]
    )

    return new_sidebar


def get_sidebar(sub):
    mod = sub.mod
    settings = mod.settings()
    sidebar_contents = settings["description"]

    return sidebar_contents


def push_sidebar(new_sidebar, sub):
    mod = sub.mod
    settings = mod.settings()

    fullname = settings.pop("subreddit_id")

    remap = {
        "allow_top": "default_set",
        "lang": "language",
        "link_type": "content_options",
    }

    for (new, old) in remap.items():
        settings[new] = settings.pop(old)

    settings.update({"description": new_sidebar})

    sub._create_or_update(_reddit=sub._reddit, sr=fullname, **settings)


def update_flairs(sub):
    for message in r.inbox.unread():
        if "change my flair text" in message.subject.lower():
            if len(message.body) <= 64:
                cssclass = sub.flair(redditor=message.author).next()["flair_css_class"]
                sub.flair.set(message.author, message.body, cssclass)

                message.reply(
                    """I've changed your flair text to **"""
                    + message.body
                    + """**! Send me a
                        new message if you want it changed again."""
                )
                message.mark_read()
            else:
                message.reply(
                    """I wasn't able to change your flair text because what you sent me
                        was longer than 64 characters. If you still want something changed, send me
                        **new** message (don't reply to this one) with something shorter!"""
                )
                message.mark_read()
        else:
            if "username mention" not in message.subject:
                message.reply(
                    """I didn't recognize the subject of your message. If you were wanting
                to change your flair text please send a message with the subject **Change My Flair Text**
                . Thanks!"""
                )
            message.mark_read()


def do_update_dota_sidebar(sidebar):
    # sidebar = update_prize_pool(sidebar)
    sidebar = update_streamers(sidebar)
    sidebar = update_matches(sidebar)
    sidebar = update_events(sidebar)

    return sidebar


def do_update_artifact_sidebar(sidebar):
    sidebar = update_artifact_streams(sidebar)
    sidebar = update_artifact_events(sidebar)
    return sidebar


def update_sidebar():
    print(time.ctime())
    print("UPDATING!")

    dota2 = r.subreddit("dota2")
    sidebar = get_sidebar(dota2)
    sidebar = do_update_dota_sidebar(sidebar)
    push_sidebar(sidebar, dota2)
    redesign.update_sidebar(dota2)

    artifact = r.subreddit("artifact")
    sidebar = get_sidebar(artifact)
    sidebar = do_update_artifact_sidebar(sidebar)
    push_sidebar(sidebar, artifact)
    redesign.update_sidebar(artifact)

    # update_flairs("dota2")


def dota_create_stupid_questions_thread():
    stupidquestions.createPost(r, "dota2", config.get("config", "STUPID_QUESTIONS_ID"))
    config.set(
        "config",
        "STUPID_QUESTIONS_ID",
        str(int(config.get("config", "STUPID_QUESTIONS_ID")) + 1),
    )

    with open("config.txt", "w") as configfile:
        config.write(configfile)


def dota_cleanup_stupid_questions_thread():
    stupidquestions.unstickyPost(r)


def artifact_create_stupid_questions_thread():
    stupidquestions.artifact_createPost(
        r, "artifact", config.get("config", "ARTIFACT_STUPID_QUESTIONS_ID")
    )
    config.set(
        "config",
        "ARTIFACT_STUPID_QUESTIONS_ID",
        str(int(config.get("config", "ARTIFACT_STUPID_QUESTIONS_ID")) + 1),
    )

    with open("config.txt", "w") as configfile:
        config.write(configfile)


def artifact_cleanup_stupid_questions_thread():
    stupidquestions.artifact_unstickyPost(r)


def create_battle_cup_thread():
    try:
        battlecup.createPost(r, "dota2")
    except Exception as e:
        print(e)


def cleanup_battle_cup_thread():
    stupidquestions.unstickyPost(r)


def create_hero_discussion_thread():
    """ Create the weekly hero discussion. No longer uses config file, instead counts previous threads.
    """
    hero_id = hero_discussion.count_prev_posts(r)
    hero_discussion.create_post(r, hero_id)

def cleanup_hero_discussion_thread():
    stupidquestions.unstickyPost(r)

def create_item_discussion_thread():
    item_id = int(config.get("config", "ITEM_DISCUSSION_ID"))
    item_discussion.create_post(r, "dota2", item_id)
    config.set("config", "ITEM_DISCUSSION_ID", str(item_discussion.next_item_index(item_id)))

    with open("config.txt", "w") as configfile:
        config.write(configfile)

def cleanup_item_discussion_thread():
    stupidquestions.unstickyPost(r)


if __name__ == "__main__":
    print("hello")
    login()

    schedule.every(30).seconds.do(update_sidebar)

    schedule.every().monday.at("16:00").do(dota_create_stupid_questions_thread)
    schedule.every().tuesday.at("16:00").do(dota_cleanup_stupid_questions_thread)

    # schedule.every().tuesday.at("17:00").do(create_hero_discussion_thread)
    # schedule.every().wednesday.at("17:00").do(cleanup_hero_discussion_thread)

    # schedule.every().thursday.at("17:00").do(create_item_discussion_thread)
    # schedule.every().friday.at("17:00").do(cleanup_item_discussion_thread)

    # schedule.every().tuesday.at("18:00").do(artifact_create_stupid_questions_thread)
    # schedule.every().wednesday.at("18:00").do(artifact_cleanup_stupid_questions_thread)

    # schedule.every().saturday.at("03:00").do(create_battle_cup_thread)
    # schedule.every().sunday.at("03:00").do(cleanup_battle_cup_thread)

    while True:
        schedule.run_pending()
        time.sleep(1)
