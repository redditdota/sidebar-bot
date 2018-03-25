import configparser
import praw
import time
import json
import random

import discord
import asyncio


config = configparser.ConfigParser()
config.read("config.txt")

subname = "dota2"
r = None

alreadySeenFilename = "alreadyseen.json"

modAuthors = ['m4rx', 'klopjobacid', 'Decency', '0Hellspawn0', 
                'crimson589', 'Intolerable', 'lestye', 'coronaria', 
                'leafeator', 'VRCkid', 'JohnScofield', 'Pohka']

alreadySeen = {}

with open(alreadySeenFilename) as file:
    alreadySeen = json.load(file)

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

        if last.author.name in modAuthors:
            continue

        body = last.body_markdown
        if len(body) > 500:
            body = body[:497] + "..."

        if last.id not in alreadySeen or alreadySeen[last.id] != True:
            alreadySeen[last.id] = False
            
            modmails.append({"kind": "new", "title": c.subject, "author": last.author.name, "body": body, "url": "https://mod.reddit.com/mail/new/" + c.id, "id": last.id})


    for c in inprogress:
        m = list(c.messages)

        if len(m) < 2:
            continue

        last = m[-1]
        prevReply = m[-2]

        if last.author.name in modAuthors:
            continue

        if last.id not in alreadySeen or alreadySeen[last.id] != True:
            alreadySeen[last.id] = False

            body = last.body_markdown
            if len(body) > 500:
                body = body[:497] + "..."

            prevBody = prevReply.body_markdown
            if len(prevBody) > 100:
                prevBody = prevBody[:97] + "..."

            modmails.append({"kind": "inprogress", "title": c.subject, "author": last.author.name, "body": body, "prevAuthor": prevReply.author.name, "prevBody": prevBody, "url": "https://mod.reddit.com/mail/inprogress/" + c.id, "id": last.id})
    
    with open(alreadySeenFilename, 'w') as file:
        json.dump(alreadySeen, file)

    print(modmails)
    return modmails

client = discord.Client()

@client.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    server = client.get_server("74287487459004416")
    #me = server.get_member_named("Vatyx")

    while True:
        print("Checking modmail")
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
            print(client.get_channel("140254555580530688"))

            message = yield from client.send_message(client.get_channel("140254555580530688"), embed=embed)
            yield from client.add_reaction(message, random.choice(server.emojis))
            
            alreadySeen[modmail["id"]] = True

            with open(alreadySeenFilename, 'w') as file:
                json.dump(alreadySeen, file)

        yield from asyncio.sleep(20)

client.run(config.get("config", "DISCORD_TOKEN"))
