import requests
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import sys
from time import time, sleep, mktime
import argparse
import csv
import os

import prospect_helper as helper
from py_db import db

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}

db = db("mlb_prospects")

sleep_time = 3
base_url = ""

start_time = time()

url_file = os.getcwd()+"/minorleagueball_urls.csv"
url_dict = {}
with open(url_file, "rU") as f:
    mycsv = csv.reader(f)
    for row in mycsv:
        year, team_abb, url = row
        try:
            int(year)
        except ValueError:
            continue
        if year not in url_dict:
            url_dict[year] = [{team_abb:url},]
        else:
            url_dict.get(year).append({team_abb:url})


def initiate(end_year, scrape_length):
    if scrape_length == "All":
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
    print "\n", year
    team_list = url_dict.get(str(year))

    for i, t in enumerate(team_list):
        team_abb, team_url = t.items()[0]
        print "\n\t", year, team_abb, i+1, "\t", team_url 
        process_team_url(year, team_abb, team_url)


def process_team_url(year, team_abb, team_url):
    sleep(sleep_time)
    html = requests.get(team_url, headers=headers)
    soup = BeautifulSoup(html.content, "lxml")


    tagged_sections = soup.findAll(["p", "class_='MsoNormal'"])
    for e in tagged_sections:
        sec_text = e.getText().strip()


        sec_text = "".join([i if ord(i) < 128 else "" for i in sec_text])
        # print sec_text

        # regex to split the text into individual player sections
        split_list = re.findall(r"\d{1,2}\) [A-Z].{0,32}['Grade','Age'].{0,32}[:.;]", sec_text)

        if split_list == []:
            continue
        # raw_input(split_list)


        sec_text = str(split_list[0]) + "".join(sec_text.split(split_list[0])[1:])

        if len(split_list) == 1:
            player_text = sec_text.split("OTHER")[0].split("Others:")[0].split("others:")[0]
            parse_player(player_text, year, team_abb)

        else:   
            for a in range(0, len(split_list)-1):
                player_text = str(split_list[a]) + sec_text.split(split_list[a])[1].split(split_list[a+1])[0].split("OTHER")[0].split("Others:")[0].split("others:")[0]
                parse_player(player_text, year, team_abb)

            a = len(split_list)-1
            player_text = str(split_list[a]) + sec_text.split(split_list[a])[1].split("OTHER")[0].split("Others:")[0].split("others:")[0]
            parse_player(player_text, year, team_abb)


def parse_player(player_text, year, team_abb):
    try:
        int(player_text[0:1])
    except ValueError:
        # raw_input(player_text)
        return None

    try:
        full_name = player_text.split(")")[1].split(",")[0].strip()
    except IndexError:
        return None

    try:
        team_rank = player_text.split(")")[0].strip()

    except IndexError:
        team_rank = None

    try:
        position = player_text.split(",")[1].split(",")[0].split(";")[0].strip().split(" ")[0].split(".")[0].strip()
    except IndexError:
        position = None

    try:
        grade_base = player_text.upper().split("GRADE")[1].split(":")[0].split(".")[0].split(";")[0]
        grade = grade_base.replace("/BORDERLINE","/").replace("BORDERLINE","/").replace("//","/").replace(" ","").strip()
    except IndexError:
        # raw_input(player_text)
        grade_base, grade = None, None


    try:
        age = player_text.lower().split(" age")[1].split(",")[0].split(";")[0].split(":")[0].split("(")[0].strip()
        age = int(age)
    except (IndexError, ValueError):
        try:
            age = player_text.lower().split("age")[1].split(",")[0].split(";")[0].strip()
            age = int(age)
        except (IndexError, ValueError):
            age = 0

    try:
        eta = player_text.lower().split(" eta")[1].split(".")[0].split(";")[0].split("(")[0].replace(":","").strip()
    except IndexError:
        eta = None

    entry = {"year":year, "team":team_abb}

    full_name, fname, lname = helper.adjust_minorleagueball_name(full_name, year, team_abb)

    est_birthyear = year - int(age)
    age = helper.adjust_minorleagueball_birthyear(full_name, year, team_abb, est_birthyear)

    position = helper.adjust_minorleagueball_position(full_name, year, team_abb, position)

    eta = helper.adjust_minorleagueball_eta(full_name, year, team_abb, eta)

    if grade is None:
        return None

    try:
        blurb = player_text.split("Grade"+grade_base+":")[1].strip()
    except (TypeError, IndexError):
        try:
            blurb = "Age " + player_text.split("Age")[1].strip()
        except (TypeError, IndexError):
            blurb = None

    try:
        grade_split = blurb.upper().split("BORDERLINE")[1].split(":")[0].split(".")[0].strip()[0:2].strip()
        if grade_split != "":
            grade = grade + "/" + grade_split
    except (IndexError, AttributeError):
        grade = grade

    grade = helper.adjust_minorleagueball_grade(full_name, year, team_abb, grade)

    if int(team_rank) == 31 and grade[0] in ("A", "B"):
        team_rank = 1

    entry["team_rank"] = team_rank
    entry["full_name"] = full_name
    entry["position"] = position
    entry["age"] = age
    entry["grade"] = grade
    entry["eta"] = eta
    entry["fname"] = fname
    entry["lname"] = lname
    entry["blurb"] = blurb
    print "\t\t", team_rank, full_name, position, age, grade, eta

    db.insertRowDict(entry, "minorleagueball_professional", replace=True, debug=1)
    db.conn.commit()


if __name__ == "__main__":     
    parser = argparse.ArgumentParser()
    parser.add_argument("--end_year",type=int,default=2018)
    parser.add_argument("--scrape_length",type=str,default="Current")

    args = parser.parse_args()
    
    initiate(args.end_year, args.scrape_length)

