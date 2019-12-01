import calendar
from datetime import datetime, timedelta
from pytz import timezone
import json
import os

import configparser
import chess

config = configparser.ConfigParser()
config.read("config.txt")

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow

dotaKey = config.get("config", "DOTA_GOOGLE_KEY")
dotaCalendarId = config.get("config", "DOTA_CALENDAR_ID")

if chess.useChessSidebar:
    dotaCalendarId = "2dpm3qirch3d7mmae04aojnu48@group.calendar.google.com"

artifactKey = config.get("config", "ARTIFACT_GOOGLE_KEY")
artifactCalendarId = config.get("config", "ARTIFACT_CALENDAR_ID")

tz = timezone('America/New_York')

def get_upcoming_events():
    service = build(serviceName='calendar', version='v3',
        developerKey=dotaKey)

    now = datetime.utcnow().isoformat() + 'Z'
    cal = service.events().list(calendarId=dotaCalendarId, timeMin=now, maxResults=5, \
             singleEvents=True, orderBy='startTime').execute()

    events = cal["items"]
    sidebar_events = []

    for event in events:
        name = event["summary"]
        #desc = event["description"].split()
        url = event["location"]

        startDate = datetime.strptime(event["start"]["date"], '%Y-%m-%d')
        endDate = datetime.strptime(event["end"]["date"], '%Y-%m-%d')
        endDate = endDate - timedelta(days=1)
        start = calendar.month_abbr[int(startDate.month)] + " " + str(int(startDate.day))
        if datetime.now() > startDate:
            start = "**Now!**"
        end = calendar.month_abbr[int(endDate.month)] + " " + str(int(endDate.day))

        sidebar_events.append({"name": name, "start": start, "end": end, "url": url})

    upcoming_events = ""
    upcoming_events += ". | .\n"
    upcoming_events += "---|---\n"
    for event in sidebar_events:
        upcoming_events += event["start"] + " - " + event["end"] + " | [" + event["name"] + "](" + event["url"] + ")\n"

    return upcoming_events

def get_upcoming_tournaments():
    service = build(serviceName='calendar', version='v3',
        developerKey=artifactKey)

    nowPlusOne = (datetime.utcnow() + timedelta(hours=1)).isoformat() + 'Z'
    cal = service.events().list(calendarId=artifactCalendarId, timeMin=nowPlusOne, maxResults=5, \
             singleEvents=True, orderBy='startTime').execute()

    events = cal["items"]
    sidebar_events = []

    for event in events:
        name = event["summary"]
        url = event["location"]

        startTime = datetime.strptime(event["start"]["dateTime"].replace(":", ""), '%Y-%m-%dT%H%M%S%z')
        nowdate  = datetime.now(tz)
        delta = startTime - nowdate
        days, hours, mins = delta.days, delta.seconds // 3600, delta.seconds // 60 % 60
        if str(days) != "0":
            time = str(days) + "d " + str(hours) + "h"
        elif str(hours) != "0":
            time = str(hours) + "h " + str(mins) + "m"
        else:
            time = str(mins) + "m"

        sidebar_events.append({"name" : name, "time": time, "url": url})

    upcoming_events = ""
    upcoming_events += ". | .\n"
    upcoming_events += "---|---\n"
    for event in sidebar_events:
        upcoming_events += event["time"] + " | [" + event["name"] + "](" + event["url"] + ")\n"

    return upcoming_events
