import configparser

import praw

import discord
import asyncio

import time

config = configparser.ConfigParser()
config.read("config.txt")

subname = "dota2"
r = None

alreadySeen = []

r = praw.Reddit(client_id=config.get("config", "CLIENT_ID"),
                client_secret=config.get("config", "CLIENT_SECRET"),
                password=config.get("config", "BOT_PASSWORD"),
                user_agent='Dota 2 sidebar bot',
                username=config.get("config", "BOT_USERNAME"))
subreddit = r.subreddit(subname)

def getModmail():
    new = subreddit.modmail.conversations(state='new')
    inprogress = subreddit.modmail.conversations(state='inprogress')

    modmails = []

    for c in new:
            m = list(c.messages)
            last = m[-1]

            if last.id not in alreadySeen:
                alreadySeen.append(last.id)
                
                modmails.append({"kind": "new", "title": c.subject, "author": last.author.name, "body": last.body_markdown, "url": "https://mod.reddit.com/mail/new/" + c.id})


    for c in inprogress:
            m = list(c.messages)

            if len(m) < 2:
                continue

            last = m[-1]
            prevReply = m[-2]

            if last.id not in alreadySeen:
                alreadySeen.append(last.id)

                modmails.append({"kind": "inprogress", "title": c.subject, "author": last.author.name, "body": last.body_markdown, "prevAuthor": prevReply.author.name, "prevBody": prevReply.body_markdown, "url": "https://mod.reddit.com/mail/inprogress/" + c.id})
    
    return modmails

client = discord.Client()

@client.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    while True:
        modmails = getModmail()

        for modmail in modmails:
            embed = discord.Embed()

            if modmail["kind"] == "new":
                embed.add_field(name = "New Modmail", value="[" + modmail["title"] + "](" + modmail["url"] + ") from [/u/" + modmail["author"] + "](https://reddit.com/u/" + modmail["author"] + ")", inline=False)
                embed.add_field(name="Body", value=modmail["body"], inline=False)


            elif modmail["kind"] == "inprogress":
                embed.add_field(name = "New Modmail Reply", value="[" + modmail["title"] + "](" + modmail["url"] + ") from [/u/" + modmail["author"] + "](https://reddit.com/u/" + modmail["author"] + ")", inline=False)

                embed.add_field(name = "Previous Reply by " + modmail["prevAuthor"], value=modmail["prevBody"], inline=False)
                embed.add_field(name = "New Reply", value=modmail["body"], inline=False)

            yield from client.send_message(client.get_channel("140254555580530688"), embed=embed)

    time.sleep(30)

client.run(config.get("config", "DISCORD_TOKEN"))