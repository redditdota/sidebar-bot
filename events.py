import calendar
import datetime
import json
import os

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow

key = os.environ["GOOGLE_KEY"]
email = os.environ["EMAIL"]

def get_upcoming_events():
    service = build(serviceName='calendar', version='v3', 
        developerKey=key)

    now = datetime.datetime.utcnow().isoformat() + 'Z'
    cal = service.events().list(calendarId=email, timeMin=now, maxResults=5, \
             singleEvents=True, orderBy='startTime').execute()

    events = cal["items"]
    sidebar_events = []

    for event in events:
        name = event["summary"]
        url = event["description"]
        startDate = datetime.datetime.strptime(event["start"]["date"], '%Y-%m-%d')
        endDate = datetime.datetime.strptime(event["end"]["date"], '%Y-%m-%d')
        start = calendar.month_abbr[int(startDate.month)] + " " + str(int(startDate.day))
        end = calendar.month_abbr[int(endDate.month)] + " " + str(int(endDate.day))

        sidebar_events.append({"name": name, "start": start, "end": end, "url": url})

    upcoming_events = ""
    upcoming_events += ". | .\n"
    upcoming_events += "---|---\n"
    for event in sidebar_events:
        upcoming_events += event["start"] + " - " + event["end"] + " | [" + event["name"] + "](" + event["url"] + ")\n"

    
    return upcoming_events

#[*Upcoming Events*](#heading)
#
#. | .
#---|---
#May 26 | [The Manila Masters](https://www.google.com)
#May 30 | [ZOTAC Cup Masters](https://www.google.com)
#June 4 | [EPICENTER 2017](https://www.google.com)
#June 14 | [DOTA Summit 7](https://www.google.com)
#June 26 | [The International 2017 Qualifiers](https://www.google.com)
#
#**[More Events](http://www.gosugamers.net/dota2/gosubet#button#slim)**
