#!/usr/bin/python3

import requests as req 
from bs4 import BeautifulSoup as bs
import json,re


def findAvailableMatches(url="http://static.cricinfo.com/rss/livescores.xml"):
    r = requests.get(url)

    soup = bs(r.text)  #it uses "html5lib" HTML parser by default
                       #might change parser on different system

    xml = soup.find_all("item")  #extracts all the item tags

    matches = map(lambda item: re.sub(r'\s+', " ",re.sub('\[^A-Za-z]+', '', item.title.text)),xml)  #return the title of each match e.g
                    #Kolkata Knight Riders v Rajasthan Royals

    return (xml, matches)
