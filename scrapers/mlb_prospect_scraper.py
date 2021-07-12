#used for seasons 2021 - present (no 2020)

import requests
import urllib
import csv
import os
import sys
import datetime
import codecs
import argparse
from time import time, sleep


from py_data_getter import data_getter
from py_db import db
import prospect_helper as helper

import NSBL_helpers as helper2


db = db("mlb_prospects")
getter = data_getter()

sleep_time = 1

# https://content-service.mlb.com/?operationName=getRankings&variables=%7B%22slug%22%3A%22sel-pr-2021-giants%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%228fa44dfe068ae49bd2fdaa2481c99685d2a73474074bfdb950791f1c70de34de%22%7D%7D

base_url = "https://content-service.mlb.com/?operationName=getRankings&variables=%%7B%%22slug%%22%%3A%%22sel-pr-%s-%s%%22%%7D&extensions=%%7B%%22persistedQuery%%22%%3A%%7B%%22version%%22%%3A1%%2C%%22sha256Hash%%22%%3A%%228fa44dfe068ae49bd2fdaa2481c99685d2a73474074bfdb950791f1c70de34de%%22%%7D%%7D"


def initiate(end_year, scrape_length):
    start_time = time()

    if scrape_length == "All":
        for year in range (2021, end_year+1):
            process(year)
    else:
        year = end_year
        process(year)

    end_time = time()
    elapsed_time = float(end_time - start_time)
    print "\n\nmlb_prospect_scraper.py"
    print "time elapsed (in seconds): " + str(elapsed_time)
    print "time elapsed (in minutes): " + str(elapsed_time/60.0)


def process(year):
    tms = db.query("SELECT mascot_name FROM NSBL.teams WHERE year = %s" % (year))
    tmlst = ["Dbacks" if tm[0]=="Diamondbacks" else tm[0] for tm in tms]
    tmlst.append("draft")
    # tmlst.append("international")

    def get_team_list(url):
        json = getter.get_url_data(url, "json")

        try:
            prospect_list = json["data"]["prospects"]
            return prospect_list
        except (KeyError):
            print("\tMISSING TEAM - waiting 30 seconds and trying again...")
            sleep(30)
            get_team_list(url)


    for i, team in enumerate(tmlst[:]):
        url = base_url % (year, team)
        print '\n', i+1, team

        empty_list = False
        while empty_list is False:
            prospect_list = get_team_list(url)

            if prospect_list is None:
                print url
            else:
                empty_list = True

        entries = []
        for j, prospect in enumerate(prospect_list):
            print "\t", j+1, prospect.get("player").get("useName"), prospect.get("player").get("lastName")
            entry = parse_prospect(j+1, year, prospect, team)
            entries.append(entry)


        if team == "draft":
            table = "mlb_prospects_draft"
        elif team == "international":
            table = "mlb_prospects_international"
        else:
            table = "mlb_prospects_professional"

        # for e in entries:
        #     for n, m in e.items():
        #         print (str(n)[:20] if len(str(i)) > 20 else str(m).ljust(20)), "\t", j
        #     raw_input("wait")
        if entries != []:
            for i in range(0, len(entries), 1000):
                db.insertRowDict(entries[i: i + 1000], table, insertMany=True, replace=True, rid=0,debug=1)
                db.conn.commit()

        # sleep(2)

def parse_prospect(rnk, year, prospect, team):
    prospect_type = (team if team in ("draft", "international") else "professional")
    entry = {}
    def print_prospect_details (prospect):
        def print_dict(k, v, lvl):
            for num in range(1, lvl):
                print "\t",
            if type(v) is dict:
                print k
                for y, z in j.items():
                    print_dict(y, z, lvl+1)
            else:
                print (str(k)[:20] if len(str(k)) > 20 else str(k).ljust(20)), "\t", ("SOME LIST" if type(v) is list else v)

        for a, b in prospect.items():
            print_dict(a, b, 1)

    def process_grades(year, grades_id, grades, player_type, prospect_type):
        grade_entry = {"year":year, "grades_id":grades_id, "prospect_type":prospect_type}
        fv = 0
        for g in grades:
            if g.get("key") is None:
                continue
            if g.get("key").lower().strip() == "overall":
                fv = g.get("value")
            elif g.get("key").lower().strip() not in ("fastball", "change", "curve", "slider", "cutter", "splitter", "control", "hit", "power", "run", "arm", "field", "speed", "throw", "defense"):
                grade_entry["other"] = g.get("value")
            else:
                if g.get("key").lower().strip() == "speed":
                    grade_entry["run"] = g.get("value")
                elif g.get("key").lower().strip() == "throw":
                    grade_entry["arm"] = g.get("value")
                elif g.get("key").lower().strip() == "defense":
                    grade_entry["field"] = g.get("value")
                else:
                    grade_entry[g.get("key").lower().strip()] = g.get("value")

        if "hit" in grade_entry or "field" in grade_entry:
            grades_table = "mlb_grades_hitters"
        elif "control" in grade_entry or "fastball" in grade_entry:
            grades_table = "mlb_grades_pitchers"
        else:
            print "\n\n\n", grades, "\n\n\n"
            return fv
        db.insertRowDict(grade_entry, grades_table, insertMany=False, replace=True, rid=0,debug=1)
        db.conn.commit()
        return fv

    # print_prospect_details(prospect)

    mlb_id = prospect.get("player").get("id")
    fname = prospect.get("player").get("useName")
    lname = prospect.get("player").get("lastName")
    input_name = fname + " " + lname
    helper2.input_name(input_name)
    fname, lname = helper.adjust_mlb_names(mlb_id, fname, lname)

    position = prospect.get("player").get("positionAbbreviation")
    position = helper.adjust_mlb_positions(mlb_id, position)

    entry["year"] = year
    entry["rank"] = rnk
    entry["mlb_id"] = mlb_id
    entry["fname"] = fname
    entry["lname"] = lname
    entry["position"] = position

    try:
        dob = prospect.get("player").get("birthDate")
        byear = dob.split("-")[0]
        bmonth = dob.split("-")[1]
        bday = dob.split("-")[2]
    except IndexError:
        print "\n\nNO BIRTHDAY", fname, lname, mlb_id, "\n\n"

    prospect_id = helper.add_prospect(mlb_id, fname, lname, byear, bmonth, bday, p_type=prospect_type)

    if prospect_id == 0 or prospect_id is None:
        grades_id = mlb_id
    else:
        grades_id = prospect_id

    entry["birth_year"] = byear
    entry["birth_month"] = bmonth
    entry["birth_day"] = bday
    entry["prospect_id"] = prospect_id
    entry["grades_id"] = grades_id

    bats = prospect.get("player").get("batSideCode")
    throws = prospect.get("player").get("pitchHandCode")
    weight = prospect.get("player").get("weight")
    try:
        height = prospect.get("player").get("height").replace("\"","").split("'")
        height = int(height[0])*12+int(height[1])
    except (IndexError, ValueError, AttributeError):
        height = None

    entry["bats"] = bats
    entry["throws"] = throws
    entry["weight"] = weight
    entry["height"] = height

    try:
        team = prospect.get("player").get("currentTeam").get("parentOrgName")
    except (AttributeError):
        team = None
    entry["team"] = team

    commit = prospect.get("prospectSchoolCommitted")
    entry["college_commit"] = commit

    eta = prospect.get("eta")
    entry["eta"] = eta

    hit_fv = None
    pitch_fv = None
    if prospect.get("gradesHitting") is not None and prospect.get("gradesHitting") != []:
        hit_grades = prospect.get("gradesHitting")
        hit_fv = process_grades(year, grades_id, hit_grades, "hit", prospect_type)

    if prospect.get("gradesPitching") is not None and prospect.get("gradesPitching") != []:
        pitch_grades = prospect.get("gradesPitching")
        pitch_fv = process_grades(year, grades_id, pitch_grades, "pitch", prospect_type)

    fv = max(hit_fv, pitch_fv)
    entry["FV"] = fv


    blurbs = prospect.get("prospectBio")
    sorted_blurbs = sorted(blurbs, key=lambda k:k["contentTitle"], reverse=True)
    cleaned_blurbs = []
    for i,b in enumerate(sorted_blurbs):
        if b.get("contentText") is None:
            sorted_blurbs[i] = None
        else:
            blurbtext = str(b.get("contentTitle")) + b.get("contentText").replace("<b>","").replace("</b>","").replace("<br />","").replace("<p>","\n").replace("</p>","").replace("*","").replace("<strong>","").replace("</strong>","")
            blurbtext = "".join([j if ord(j) < 128 else "" for j in blurbtext])
            cleaned_blurbs.append(blurbtext)

    blurb = "\n\n".join(cleaned_blurbs)
    entry["blurb"] = blurb

    # raw_input(entry)
    return entry



if __name__ == "__main__":     
    parser = argparse.ArgumentParser()
    parser.add_argument("--end_year",type=int,default=2021)
    parser.add_argument("--scrape_length",type=str,default="Current")

    args = parser.parse_args()
    
    initiate(args.end_year, args.scrape_length)

