import calendar
from datetime import datetime, timedelta
import json
import os

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow

key = os.environ["GOOGLE_KEY"]
email = os.environ["EMAIL"]
calendar_id = os.environ["CALENDAR_ID"]

def get_upcoming_events():
    service = build(serviceName='calendar', version='v3', 
        developerKey=key)

    now = datetime.utcnow().isoformat() + 'Z'
    cal = service.events().list(calendarId=calendar_id, timeMin=now, maxResults=5, \
             singleEvents=True, orderBy='startTime').execute()

    events = cal["items"]
    sidebar_events = []

    for event in events:
        name = event["summary"]
        url = event["description"].split()[-1]
        print(event["description"].split())

        startDate = datetime.strptime(event["start"]["date"], '%Y-%m-%d')
        endDate = datetime.strptime(event["end"]["date"], '%Y-%m-%d')
        endDate = endDate - timedelta(days=1)
        start = calendar.month_abbr[int(startDate.month)] + " " + str(int(startDate.day))
        end = calendar.month_abbr[int(endDate.month)] + " " + str(int(endDate.day))

        sidebar_events.append({"name": name, "start": start, "end": end, "url": url})

    upcoming_events = ""
    upcoming_events += ". | .\n"
    upcoming_events += "---|---\n"
    for event in sidebar_events:
        upcoming_events += event["start"] + " - " + event["end"] + " | [" + event["name"] + "](" + event["url"] + ")\n"

    
    return upcoming_events