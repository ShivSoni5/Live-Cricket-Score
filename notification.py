#!/usr/bin/python3

from os import system
#import sys
from subprocess import call

def message(title, score):
#        system("notify-send -u critical {} {}".format(title, score))
        call(['notify-send','-u','normal', title, score])
