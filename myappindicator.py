#!/usr/bin/env python

# This code is an example for a tutorial on Ubuntu Unity/Gnome AppIndicators:
# http://candidtim.github.io/appindicator/2014/09/13/ubuntu-appindicator-step-by-step.html

import os
import signal
import json
import gi
import requests
import datetime

from urllib2 import Request, urlopen, URLError

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify
from itertools import groupby
from collections import namedtuple

APPINDICATOR_ID = 'myappindicator'

Result = namedtuple("Result", "homeTeam, goalsHomeTeam, awayTeam, goalsAwayTeam")

def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID,  os.path.abspath('/home/adi/Developments/python/dock/football-icon-65993.png'), appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    gtk.main()

def build_menu():
    menu = gtk.Menu()
    item_joke = gtk.MenuItem('Live Score')
    item_joke.connect('activate', joke)
    menu.append(item_joke)
    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu

def joke(_):
    notify.Notification.new("<b>Live Score</b>", live_scores(), None).show()

def quit(_):
    notify.uninit()
    gtk.main_quit()

def live_scores():
    LIVE_URL = 'http://soccer-cli.appspot.com/'
    """Gets the live scores"""
    req = requests.get(LIVE_URL)
    if req.status_code == requests.codes.ok:
	live_scores = req.json()
	str = ''
	"""Prints the live scores in a pretty format"""
        live_scores = sorted(live_scores["games"], key=lambda x: x["league"])
        for league, games in groupby(live_scores, key=lambda x: x["league"]):
        #str+='{:}\n'.format(league)
        #str+='----------------------------------------------\n'
            for game in games:
                result = parse_result(game)
                left_score='{:} {:}'.format(result.goalsHomeTeam, result.homeTeam.encode('utf-8').strip())
                str+='{:{text_width}} {:{align}{text_width}}\t'.format(convert_utc_to_local_time(game["time"]), left_score, align='<', text_width='10')
                str+='{:{align}} {:{align}{text_width}}\n'.format(result.goalsAwayTeam, result.awayTeam.encode('utf-8').strip(), text_width='20', align='<')
        #str+='---------------------------------------------\n'
        return str

    if len(live_scores["games"]) == 0:
	    return "No live action currently"
    else:
	    return "There was problem getting live scores"

def parse_result(data):
    """Parses the results and returns a Result namedtuple"""
    def valid_score(score):
        return "-" if score == -1 else score

    if "result" in data:
        result = Result(
            data["homeTeamName"],
            valid_score(data["result"]["goalsHomeTeam"]),
            data["awayTeamName"],
            valid_score(data["result"]["goalsAwayTeam"]))
    else:
        result = Result(
            data["homeTeamName"],
            valid_score(data["goalsHomeTeam"]),
            data["awayTeamName"],
            valid_score(data["goalsAwayTeam"]))

    return result

def convert_utc_to_local_time(time_str, show_datetime=False):
    """Converts the API UTC time string to the local user time."""
    if not (time_str.endswith(" UTC") or time_str.endswith("Z")):
        return time_str

    today_utc = datetime.datetime.utcnow()
    utc_local_diff = today_utc - datetime.datetime.now()
    
    if time_str.endswith(" UTC"):
        time_str, _ = time_str.split(" UTC")
        utc_time = datetime.datetime.strptime(time_str, '%I:%M %p')
        utc_datetime = datetime.datetime(today_utc.year, today_utc.month, today_utc.day,
                                            utc_time.hour, utc_time.minute)
    else:
        utc_datetime = datetime.datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%SZ')
        
    local_time = utc_datetime - utc_local_diff
    
    date_format = '%I:%M %p' if not show_datetime else '%a %d, %I:%M %p'
    return datetime.datetime.strftime(local_time, date_format)


    

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
