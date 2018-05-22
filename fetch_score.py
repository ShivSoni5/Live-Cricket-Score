#!/usr/bin/python3

import requests as req 
from bs4 import BeautifulSoup as bs
import json,re


def findAvailableMatches(url="http://static.cricinfo.com/rss/livescores.xml"):
    r = req.get(url)

    soup = bs(r.text,"html5lib")  #it uses "html5lib" HTML parser by default
                       #might change parser on different system

    xml = soup.find_all("item")  #extracts all the item tags

    matches = map(lambda item: re.sub(r'\s+', " ",re.sub('\[^A-Za-z]+', '', item.title.text)),xml)  #return the title of each match e.g
                    #Kolkata Knight Riders v Rajasthan Royals

    return (xml, matches)

def getMatchID(matchChoice, xml):
    guid = xml[matchChoice].guid.text
    matchID = re.search(r'\d+',guid).group()
    return matchID

def get_JSON_URL(matchID):
    jsonurl = "http://www.espncricinfo.com/ci/engine/match/" + matchID + ".json"
    return jsonurl

def get_Playing_Team_Names(jsonurl):
    r = req.get(jsonurl)
    jsonData = r.json()
    playingTeams = {team.get("team_id"):team.get("team_name") for team in jsonData.get("team")}
    return playingTeams
