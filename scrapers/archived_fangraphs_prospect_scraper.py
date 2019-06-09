import requests
import urllib2
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import sys
from time import time, sleep, mktime
import argparse


from py_db import db
import prospect_helper as helper


db = db("mlb_prospects")


sleep_time = 3
base_url = "https://www.fangraphs.com/scoutboard.aspx"
current_page = 1


start_time = time()


def initiate(end_year, scrape_length):
    if scrape_length == 'All':
        for year in range (2013, end_year+1):
            process(year)
    else:
        year = end_year
        process(year)


    end_time = time()
    elapsed_time = float(end_time - start_time)
    print "\n\nfangraphs_prospect_scraper.py"
    print "time elapsed (in seconds): " + str(elapsed_time)
    print "time elapsed (in minutes): " + str(elapsed_time/60.0)


def process(year):
    # for list_type, list_key in {"draft":"mlb","professional":"prospect","international":"int"}.items():
    for list_type, list_key in {"draft":"mlb"}.items():


        if ((list_type=="professional" and year > 2016) or 
            (list_type=="draft" and year > 2014) or 
            (list_type=="international" and year > 2014)):
            process_prospect_list(year, list_type, list_key)


def process_prospect_list(year, list_type, list_key):
    players_per_page = 10
    list_url = base_url +"?draft=%s%s&page=1_%s" % (year, list_key, players_per_page)
    print "\n", year, list_type, list_url

    sleep(sleep_time)
    page_data = requests.get(list_url)
    soup = BeautifulSoup(page_data.content, "lxml")

    try:
        total_pages = soup.find(class_="rgWrap rgInfoPart").findAll("strong")
        pages_cnt = total_pages[1].getText()
    except AttributeError:
        pages_cnt = 1

    # for page in range(1 ,int(pages_cnt)+1):
    for page in range(current_page ,int(pages_cnt)+1):
        list_sub_url = base_url + "?draft=%s%s&page=%s_%s"% (year, list_key, page, players_per_page)
        print "\t", list_sub_url

        process_list_page(year, list_type, list_key, list_sub_url, page, players_per_page, players_per_page*int(pages_cnt))


def process_list_page(year, list_type, list_key, list_sub_url, page, players_per_page, max_players):
    sleep(sleep_time)
    page_data = requests.get(list_sub_url)
    soup = BeautifulSoup(page_data.content, "lxml")

    entries = []
    rows = soup.findAll(True, {"class":["rgRow","rgAltRow"]})
    for cnt, row in enumerate(rows):
        if list_type == "professional":
            process_professional(year, row, (page-1)*players_per_page+cnt+1, max_players)
        else:
            process_amateur(year, row, list_type, (page-1)*players_per_page+cnt+1, max_players)


def process_professional(year, row, cnt, max_players):
    entry = {}

    elements = row.findAll(True, {"class":["grid_line_regular", "grid_line_break"]})

    full_name = elements[0].getText()
    if full_name.strip() == "":
        return None

    full_name, fname, lname = helper.adjust_fg_names(full_name)

    prospect_url_base = "https://www.fangraphs.com/"
    if full_name == "Shohei Ohtani":
        prospect_url = "https://www.fangraphs.com/statss.aspx?playerid=19755&position=P"
    else:
        try:
            prospect_url = prospect_url_base + row.find("a", href=True)["href"].split("&")[0]
        except TypeError:
            prospect_url = ""

    if "statss.aspx" not in prospect_url:
        # print "\n\n**ERROR TAG** NO BIRTHDAY", year, full_name, "\n\n"
        prospect_url = None

    print "\t\t", year, str(cnt) + " of " + str(max_players), full_name, "\t", prospect_url

    if prospect_url is not None:
        birth_year, birth_month, birth_day, overall_rank, team_rank, reported, scouting_dict = process_fangraphs_url(prospect_url)

        fg_id = prospect_url.split("playerid=")[-1]
        fg_id, birth_year, birth_month, birth_day = helper.adjust_fg_birthdays(fg_id, birth_year, birth_month, birth_day)
    
        prospect_id = helper.add_prospect(fg_id, fname, lname, birth_year, birth_month, birth_day, "fg")
    else:
        birth_year, birth_month, birth_day, overall_rank, team_rank, reported, scouting_dict = None, None, None, None, None, None, None
        age = int(elements[7].getText())

        low_year = year-age-0
        up_year = year-age+0
        prospect_id, byear, bmonth, bday = helper.id_lookup(fname, lname, low_year, up_year)

        if prospect_id == 0:
            low_year = year-age-1
            up_year = year-age+1
            prospect_id, byear, bmonth, bday = helper.id_lookup(fname, lname, low_year, up_year)

            if prospect_id == 0:
                low_year = year-age-2
                up_year = year-age+2
                prospect_id, byear, bmonth, bday = helper.id_lookup(fname, lname, low_year, up_year)

        fg_id = str(year) + '_' + fname + '_' + lname

    entry["prospect_id"] = prospect_id
    entry["year"] = year
    entry["birth_year"] = birth_year
    entry["birth_month"] = birth_month
    entry["birth_day"] = birth_day


    element_dict = {1:"team", 3:"top100", 4:"team_rank", 5:"FV", 6:"ETA", 9:"weight", 10:"bats", 11:"throws", 12:"signed"}
    for i, e in enumerate(elements):
        if i in element_dict:
            i_val = element_dict.get(i)
            entry[i_val] = e.getText()

    entry["full_name"] = full_name
    entry["fname"] = fname
    entry["lname"] = lname

    if entry["top100"] == 0:
        entry["top100"] == None

    try:
        position = elements[2].getText()
    except TypeError:
        position = None
    position = helper.adjust_fg_positions(full_name, position)
    entry["position"] = position

    try:
        signed_from = elements[13].getText()
    except TypeError:
        signed_from = None
    entry["signed_from"] = signed_from

    try:
        height = elements[8].getText()
        height = int(height.split("'")[0])*12 + int(height.split("'")[1].split("\"")[0])
    except ValueError:
        height = 0
    entry["height"] = height

    try:
        video = row.find(class_ = "fancybox-media")["href"].strip()
    except TypeError:
        video = None
    entry["video"] = video

    if scouting_dict is not None:
        process_scouting_grades(reported, fg_id, scouting_dict)

    entry["fg_id"] = fg_id.split("&")[0]

    db.insertRowDict(entry, "fg_prospects_professional", replace=True, debug=1)


def process_amateur(year, row, list_type, cnt, max_players):
    entry = {"year":year}

    elements = row.findAll(True, {"class":["grid_line_regular", "grid_line_break"]})

    if list_type == "draft":
        element_dict = {0:"rank", 1:"top100", 7:"weight", 8:"bats", 9:"throws", 10:"school", 11:"college_commit", 12:"athleticism", 13:"frame", 14:"performance", 15:"fv", 16:"risk", 18:"video"}
        pick_index = 2
        name_index = 3
        position_index = 4
        age_index = 5
        age_name = "draft_age"
        height_index = 6
        blurb_index = 17
    elif list_type == "international":
        element_dict = {0:"rank", 4:"country", 5:"height", 6:"weight", 7:"bats", 8:"throws", 9:"fv", 10:"risk", 11:"proj_team", 13:"video"}
        name_index = 1
        position_index = 2
        age_index = 3
        age_name ="j2_age"
        height_index = 5
        blurb_index = 12

    for i, e in enumerate(elements):
        if i in element_dict:
            i_val = element_dict.get(i)
            if i_val == "video":
                try:
                    url = e.find("a", href=True)["href"]
                except TypeError:
                    url = ""
                entry[i_val] = url
            else:
                entry[i_val] = e.getText()

    full_name = elements[name_index].getText().replace("**","")
    full_name, fname, lname = helper.adjust_fg_names(full_name)
    print "\t\t", year, list_type, str(cnt) + " of " + str(max_players), full_name

    age = elements[age_index].getText()
    age = helper.adjust_fg_age(full_name, year, list_type, age)
    try:
        lower_year, upper_year = helper.est_fg_birthday(age, year, list_type)
        est_years = str(lower_year) + "-" + str(upper_year)

        low_year = lower_year+1
        up_year = upper_year-1
        prospect_id, byear, bmonth, bday = helper.id_lookup(fname, lname, low_year, up_year)

        if prospect_id == 0:
            low_year = lower_year
            up_year = upper_year
            prospect_id, byear, bmonth, bday = helper.id_lookup(fname, lname, low_year, up_year)

            if prospect_id == 0:
                low_year = lower_year-1
                up_year = upper_year+1
                prospect_id, byear, bmonth, bday = helper.id_lookup(fname, lname, low_year, up_year)

    except ValueError:
        est_years = "0-0"
        prospect_id = 0

    try:
        height = elements[height_index].getText()
        height = int(height.split("'")[0])*12 + int(height.split("'")[1].split("\"")[0])
    except ValueError:
        height = 0

    position = elements[position_index].getText()
    position = helper.adjust_fg_positions2(full_name, position)

    try:
        blurb_split = "Report"+elements[name_index].getText()
        blurb = elements[blurb_index].getText().split(blurb_split)[1]
        blurb = "".join([i if ord(i) < 128 else "" for i in blurb])
    except IndexError:
        blurb = ""

    blurb = blurb.replace("TLDR", "Brief:\n").replace("Full Report", "\n\nFull Report:\n")

    if "-" in entry["fv"]:
        print entry["fv"]
        entry["fv"] = int(str(entry["fv"])[0:-1]) - 2
    elif "+" in entry["fv"]:
        entry["fv"] = int(str(entry["fv"])[0:-1]) + 2

    if list_type == "draft":
        try:
            pick_detail = elements[pick_index].getText()
            pick_team = pick_detail.split("/")[0]
            pick_num = pick_detail.split("/")[1]
        except IndexError:
            pick_team = None
            pick_num = None

        entry["pick_team"] = pick_team
        entry["pick_num"] = pick_num

    entry["full_name"] = full_name
    entry["fname"] = fname
    entry["lname"] = lname
    entry[age_name] = age
    entry["est_years"] = est_years
    entry["prospect_id"] = prospect_id
    entry["height"] = height
    entry["position"] = position
    entry["blurb"] = blurb


    if list_type == "draft":
        table = "fg_prospects_draft"
    elif list_type == "international":
        table = "fg_prospects_international"

    db.insertRowDict(entry, table, replace=True, debug=1)
    db.conn.commit()


def process_fangraphs_url(player_url):
    sleep(sleep_time)
    player_data = requests.get(player_url)
    player_utf_data = "".join([i if ord(i) < 128 else "" for i in player_data.content])

    player_soup = BeautifulSoup(player_utf_data, "lxml")

    try:
        birthdate = player_soup.find(class_ = "player-info-bio").getText().split("Birthdate: ")[1].split("(")[0].strip()
        birth_month, birth_day, birth_year = birthdate.split("/")
    except ValueError:
        return None, None, None, None, None, None, None

    try:
        report_info = player_soup.find(class_ = "prospects-report").find("span")
        report_string = str(report_info)
    except AttributeError:
        return birth_year, birth_month, birth_day, None, None, None, None

    team_rank, overall_rank, reported = None, None, None
    team_rank = report_string.split("Team Rank</strong>:")[1].split("<strong")[0].strip()
    overall_rank = report_string.split("Overall Rank</strong>:")[1].split("<strong")[0].strip()
    reported = report_string.split("Reported</strong>:")[1].split("<strong")[0].strip()

    scouting_table_soup = player_soup.find(class_ = "depth_chart")
    scouting_table = scouting_table_soup.findAll("tr")
    prospect_categories = scouting_table[0].findAll("th")
    prospect_values = scouting_table[1].findAll("td")

    cats = {}
    for i, cat in enumerate(prospect_categories):
        cats[i] = cat.getText()

    scouting_dict = {}
    vals = {}
    for i, val in enumerate(prospect_values):
        cat = cats.get(i)
        scouting_dict[cat] = val.getText()

    return birth_year, birth_month, birth_day, overall_rank, team_rank, reported, scouting_dict    


def process_scouting_grades(reported, fg_id, scouting_dict):
    entry = {}
    if "Hit" in scouting_dict:
        player_type = "hitters"
    elif ("Fastball" in scouting_dict or "Command" in scouting_dict):
        player_type = "pitchers"
    else:
        # print "\n\n**ERROR TAG** CORRUPTED GRADES", reported, fg_id, scouting_dict, "\n\n"
        return None

    entry["year"] = reported
    entry["fg_id"] = fg_id.split("&")[0]

    hitter_cats = ["Hit", "GamePower", "Field", "RawPower", "Speed", "Throws"]
    pitcher_cats = ["Fastball", "Changeup", "Curveball", "Slider", "Cutter", "Splitter", "Command"]
    for k, v in scouting_dict.items():
        if player_type == "hitters":
            if k in hitter_cats:
                grade_present = v.split(" / ")[0].strip()
                grade_future = v.split(" / ")[1].strip()
                if grade_present < 8:
                    grade_present = grade_present*10
                if grade_future < 8:
                    grade_future = grade_future*10
                entry[k+"_present"] = grade_present
                entry[k+"_future"] = grade_future
            elif k != "Future Value":
                print "\n\n**ERROR TAG** NO CATEGORY", k, "\t", v, "\n\n"
        elif player_type == "pitchers":
            if k in pitcher_cats:
                grade_present = v.split(" / ")[0].strip()
                grade_future = v.split(" / ")[1].strip()
                if grade_present < 8:
                    grade_present = grade_present*10
                if grade_future < 8:
                    grade_future = grade_future*10
                entry[k+"_present"] = grade_present
                entry[k+"_future"] = grade_future
            elif k != "Future Value":
                grade_present = v.split(" / ")[0].strip()
                grade_future = v.split(" / ")[1].strip()
                if grade_present < 8:
                    grade_present = grade_present*10
                if grade_future < 8:
                    grade_future = grade_future*10
                entry["Other_present"] = grade_present
                entry["Other_future"] = grade_future

    table = "fg_grades_%s" % (player_type)
    db.insertRowDict(entry, table, replace=True, debug=1)
    db.conn.commit()


if __name__ == "__main__":     
    parser = argparse.ArgumentParser()
    parser.add_argument("--end_year",type=int,default=2018)
    parser.add_argument("--scrape_length",type=str,default="Current")

    args = parser.parse_args()
    
    initiate(args.end_year, args.scrape_length)

