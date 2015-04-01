#!/usr/bin/python3
import requests
import lxml.html
from comfy.models import Match, User, Team

def scrape():
    return_matches = []
    r = requests.get("http://csgolounge.com")
    if r.status_code != 200:
        return
    html = lxml.html.document_fromstring(r.text)

    matches = html.find_class("matchmain")

    for match in matches:
        available = True
        if match.find_class("notavailable"):
            available = False

        matchleft = match.find_class("matchleft")[0]
        team_div = matchleft.find_class("team")
        teams = matchleft.find_class("teamtext")
        links = matchleft.iterlinks()
        for l in links:
            id = l[2].strip("match?m=")
            break

        team_1_name = teams[0][0].text_content()
        team_1_odds = teams[0][2].text_content().strip("%")
        team_1_won = len(team_div[0]) > 0

        team_2_name = teams[1][0].text_content()
        team_2_odds = teams[1][2].text_content().strip("%")
        team_2_won = len(team_div[1]) > 0

        when = match.find_class("whenm")[0].text_content().strip('Â\xa0Â\xa0\r\n').strip('Â\xa0Â\xa0a')
        live = False

        if "LIVE" in when:
            live = True

        event = match.find_class("eventm")[0].text_content()

        match_details = {
            "available" : available,
            "id" : id,
            "team_1_name" : team_1_name,
            "team_1_odds" : team_1_odds,
            "team_1_won" : team_1_won,
            "team_2_name" : team_2_name,
            "team_2_odds" : team_2_odds,
            "team_2_won" : team_2_won,
            "when" : when,
            "live" : live,
            "event" : event,
        }
        return_matches.append(match_details)
    return return_matches

def handle_match_info(match_details):
    match, match_is_new = Match.objects.get_or_create(pk=match_details["id"])
    print("Match {}, is new: {}".format(match.id,match_is_new))
    if match_is_new:
        match.team_1, team_1_is_new = Team.objects.get_or_create(name=match_details["team_1_name"])
        match.team_2, team_2_is_new = Team.objects.get_or_create(name=match_details["team_2_name"])

    match.odds_1 = match_details["team_1_odds"]
    match.odds_2 = match_details["team_2_odds"]

    match.time = match_details["when"]

    if match.state == match.OPEN:
        if match_details["live"] == True:
            print("Match ID = {} is now LIVE".format(match.id))
            match.state = match.LIVE

    if match.state != match.PROCESSED:
        if match_details["available"] == False:
            print("Match ID = {} is now DONE".format(match.id))
            match.state = match.FINISHED
            if match_details["team_1_won"]:
                match.winner = Match.TEAM_1_WIN
                print("Match ID = {}, team {} wins!".format(match.id,match.team_1.name))
            elif match_details["team_2_won"]:
                match.winner = Match.TEAM_2_WIN
                print("Match ID = {}, team {} wins!".format(match.id,match.team_2.name))
            else:
                print("Match ID = {}, match was closed.".format(match.id))
                match.winner = Match.CLOSED
            match.run_bets()
    match.save()

def full_cycle():
    match_details = scrape()
    for match in match_details:
        handle_match_info(match)
