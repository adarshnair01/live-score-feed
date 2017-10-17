
import requests
import datetime
from itertools import groupby
from collections import namedtuple

import constants


def live_scores():
    """Gets the live scores"""
    req = requests.get(constants.LIVE_URL)
    if req.status_code == requests.codes.ok:
        live_scores = req.json()
        str = ""
        """Prints the live scores in a pretty format"""
        live_scores = sorted(live_scores["games"], key=lambda x: x["league"])
        for league, games in groupby(live_scores, key=lambda x: x["league"]):
            for game in games:
                result = parse_result(game)
                left_score = '{:} {:}'.format(result.goalsHomeTeam, result.homeTeam.encode('utf-8').strip())
                str += '{:{text_width}} {:{align}{text_width}}\t'.format(convert_utc_to_local_time(game["time"]),
                                                                         left_score, align='<', text_width='10')
                str += '{:{align}} {:{align}{text_width}}\n'.format(result.goalsAwayTeam,
                                                                    result.awayTeam.encode('utf-8').strip(),
                                                                    text_width='20', align='<')
        return str

        if len(live_scores["games"]) == 0:
            return "No live action currently"
        else:
            return "There was problem getting live scores"



def valid_score(score):
    return "-" if score == -1 else score

def parse_result(data):
    """Parses the results and returns a Result namedtuple"""

    Result = namedtuple("Result", "homeTeam, goalsHomeTeam, awayTeam, goalsAwayTeam")

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

