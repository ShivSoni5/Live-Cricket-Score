#!/usr/bin/env python3

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

def getLatestScore(jsonurl, playingTeams):
    r = req.get(jsonurl)
    jsonData = r.json()
    matchStatus = jsonData.get("live").get("status")
    titleDisplay = matchStatus
    scoreDisplay = ""

    if(not jsonData.get("live").get("innings")):
        return (titleDisplay,scoreDisplay)

    if("won by" in matchStatus):
        return(titleDisplay,scoreDisplay)

    innings = jsonData.get("live").get("innings")
    batting_team_id = innings.get("batting_team_id")
    battingTeamName = playingTeams[batting_team_id]
    bowling_team_id = innings.get("bowling_team_id")
    bowlingTeamName = playingTeams[bowling_team_id]
    overs = innings.get("overs")
    runs = innings.get("runs")
    wickets = innings.get("wickets")
    
    try:
        requiredRuns = jsonData.get("comms")[1].get("required_string")
    except IndexError:
        requiredRuns = ""

    titleToDisplay = battingTeamName + " vs " + bowlingTeamName + "🏏"
    scoreToDisplay = "score: " + runs + "/" + wickets +"\n" +"overs: " + overs+ "\n" + requiredRuns
    return (titleToDisplay, scoreToDisplay)

