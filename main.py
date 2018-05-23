#!/usr/bin/env python3

import fetch_score as fs  #call fetch_score.py
import sys 
from time import sleep
import notification as notify  #call notification.py

def exitApp():
    print("Thanks for using 😇")
    sys.exit()

def main():
    while True:
        xml, matches = fs.findAvailableMatches()
#       print(list(matches))
        matches = list(matches)
        if (matches[0] == "No Match in progress") :
            print("No Live matches are available now!😟" )
            exitApp()

        else :
            for matchID , match in enumerate(matches):
                print(matchID,match)

            try:
                matchChoice = int(input("Enter Match Index to get its score: "))

            except KeyboardInterrupt:
                exitApp()

            matchID = fs.getMatchID(matchChoice, xml)
#            print (matchID)

            jsonurl = fs.get_JSON_URL(matchID)       
#            print(jsonurl)

            playingTeams = fs.get_Playing_Team_Names(jsonurl)
#            print(playingTeams)

            while True:
                try:
                    title, score = fs.getLatestScore(jsonurl, playingTeams)
#                    print (title,score)
#                    system("notify-send -u critical {} {}".format(title,score))
                    notify.message(title,score)
                    sleep(60)
                except KeyboardInterrupt:
                    break
if __name__ == '__main__':
    main()
