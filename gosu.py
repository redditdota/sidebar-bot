import urllib2
from bs4 import BeautifulSoup

import datetime
import dateutil.parser
import requests

tables = None

count = 0
sidebar_matches = []

apiKey = ""

def get_gosu_matches():
    url = "http://www.gosugamers.net/api/matches?apiKey=" + apiKey + "&game=dota2&maxresults=5"

    nowdate  = datetime.datetime.fromtimestamp(float(datetime.datetime.utcnow().strftime('%s')))

    r = requests.get(url)

    matches = r.json()["matches"][:5]

    for match in matches:

        isLive = match["isLive"]
        matchUrl = match["pageUrl"]

        team1 = match["firstOpponent"]["shortName"]
        re1 = match["firstOpponent"]["country"]["countryCode"]

        team2 = match["secondOpponent"]["shortName"]
        re2 = match["secondOpponent"]["country"]["countryCode"]

        tournament = match["tournament"]["name"]

        time = None
        if isLive:
            time = "LIVE"
        else:
            dt = match["datetime"]
            gamedate = datetime.datetime.fromtimestamp(float(dateutil.parser.parse(dt).strftime('%s')))
            delta = gamedate - nowdate
            days, hours, mins = delta.days, delta.seconds // 3600, delta.seconds // 60 % 60

            if days == "0":
                time = str(days) + "d " + str(hours) + "h"
            else:
                time = str(hours) + "h " + str(mins) + "m"

        sidebar_matches.append({"team1": team1, "team2": team2, "region1": re1.lower(), "region2":
            re2.lower(), "tournament": tournament, "time": time, "link": matchUrl})


#def fetch_match_tables():
#    global tables
#
#    gosu = "http://www.gosugamers.net/dota2/gosubet"
#    page = urllib2.urlopen(gosu)
#    soup = BeautifulSoup(page, "html.parser")
#
#    tables = soup.findAll("table", attrs={'class': 'simple matches'})
#
#def scrap_live_match(table):
#    global count
#
#    rows = table.findAll('tr')
#    for row in rows:
#        if count > 5:
#            return
#
#        opp1 = row.find("span", attrs={'class': 'opp1'})
#        opp1children = opp1.findChildren()
#        team1 = opp1children[0].text
#        re1 = opp1children[1].attrs['class'][1]
#
#        opp2 = row.find("span", attrs={'class': 'opp2'})
#        opp2children = opp2.findChildren()
#        team2 = opp2children[1].text
#        re2 = opp2children[0].attrs['class'][1]
#
#        link = row.find("a", attrs={'class': 'match'})
#        link = link.attrs['href']
#
#        matches.append({"team1": team1, "team2": team2, "region1": re1.lower(), "region2": re2.lower(), "time": "LIVE", "link": link})
#        count += 1
#
#def scrap_upcoming_match(table):
#    global count
#
#    rows = table.findAll('tr')
#    for row in rows:
#        if count > 5:
#            return
#
#        opp1 = row.find("span", attrs={'class': 'opp1'})
#        opp1children = opp1.findChildren()
#        team1 = opp1children[0].text
#        re1 = opp1children[1].attrs['class'][1]
#
#        opp2 = row.find("span", attrs={'class': 'opp2'})
#        opp2children = opp2.findChildren()
#        team2 = opp2children[1].text
#        re2 = opp2children[0].attrs['class'][1]
#
#        timespan = row.find("span", attrs={'class': 'live-in'})
#        time = timespan.text.strip()
#
#        link = row.find("a", attrs={'class': 'match'})
#        link = link.attrs['href']
#
#        matches.append({"team1": team1, "team2": team2, "region1": re1.lower(), "region2": re2.lower(), "time": time, "link": link})
#        count += 1

def format_matches():
    formatted_matches = []

    for match in sidebar_matches:
        sidebarmatch = ""
        
        sidebarmatch += ">>>[~~" + match["tournament"] + "~~\n"
        sidebarmatch += "~~" + match["time"] + "~~\n"
        sidebarmatch += "~~" + match["team1"] + "~~\n"
        sidebarmatch += "~~" + match["team2"] + "~~](" + match["link"] + ")\n"
        sidebarmatch += "[](/" + match["region1"] + ")\n"
        sidebarmatch += "[](/" + match["region2"] + ")\n"
        sidebarmatch += "\n[](#separator)\n\n"

        formatted_matches.append(sidebarmatch)
    
    return "".join(formatted_matches)


def get_matches():
    get_gosu_matches()

    return format_matches()
