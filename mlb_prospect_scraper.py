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


db = db("mlb_prospects")
getter = data_getter()

sleep_time = 0

base_url = "http://m.mlb.com/gen/players/prospects/%s/playerProspects.json"
player_base_url = "http://m.mlb.com/gen/players/prospects/%s/%s.json"
player2_base_url = "http://mlb.com/lookup/json/named.player_info.bam?sport_code='mlb'&player_id=%s"


def initiate(end_year, scrape_length):
    start_time = time()

    if scrape_length == "All":
        for year in range (2013, end_year+1):
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
    url = base_url % year
    print(url)
    json = getter.get_url_data(url, "json")
    prospect_lists = json["prospect_players"]
    scrape_prospects(year, prospect_lists)


def scrape_prospects(year, prospect_lists):

    list_cnt = 0
    for list_type in (prospect_lists):
        entries = []
        if list_type not in ("rule5", "prospects", "pdp", "rhp", "lhp", "c", "1b", "2b", "3b", "ss", "of"):
        # if list_type in ("draft","int"):
            list_cnt += 1
            ind_list = prospect_lists[list_type]
            
            i = 0
            for player in ind_list:
                entry = {}
                i += 1
                sleep(sleep_time)
                mlb_id = player["player_id"]
                player_url = player_base_url % (year, mlb_id)
                
                print list_cnt, year, list_type, "\t", str(mlb_id)
                print "\t\t", str(player_url)

                sleep(sleep_time)
                player_json = getter.get_url_data(player_url, "json")

                try:
                    player_info = player_json["prospect_player"]
                except TypeError:
                    print "\n\n**ERROR TAG** TYPE_ERROR", str(year), str(mlb_id), "\n\n"
                    continue

                fname = player_info["player_first_name"]
                lname = player_info["player_last_name"]
                fname, lname = helper.adjust_mlb_names(mlb_id, fname, lname)

                position = player_info["positions"]
                position = helper.adjust_mlb_positions(mlb_id, position)

                entry["year"] = year
                entry["rank"] = i
                entry["mlb_id"] = mlb_id
                entry["fname"] = fname
                entry["lname"] = lname
                entry["position"] = position

                if list_type in ("int","draft"):
                    bats = player_info["bats"]
                    throws = player_info["thrw"]
                    try:
                        height = player_info["height"].replace("\"","").split("\"")
                        height = int(height[0])*12+int(height[1])
                    except (IndexError, ValueError, AttributeError):
                        height = None
                    weight = player_info["weight"]
                    try:
                        dob = player_info["birthdate"]
                        byear = dob.split("/")[2]
                        bmonth = dob.split("/")[0]
                        bday = dob.split("/")[1]
                    except IndexError:
                        print '\n\nNO BIRTHDAY', fname, lname, mlb_id, "\n\n"
                        continue

                    byear, bmonth, bday = helper.adjust_mlb_birthdays(mlb_id, byear, bmonth, bday)

                    prospect_id = helper.add_prospect(mlb_id, fname, lname, byear, bmonth, bday, p_type=list_type)

                else:
                    info_url = player2_base_url % mlb_id
                    print "\t\t", info_url

                    sleep(sleep_time)
                    info_json = getter.get_url_data(info_url, "json", json_unicode_convert=True)
                    try:
                        info_info = info_json["player_info"]["queryResults"]["row"]
                    except TypeError:
                        print "\n\n**ERROR TAG** MLB_ERROR", str(year), str(mlb_id), str(fname), str(lname), "\n\n"
                        continue
                        
                    dob = info_info["birth_date"]
                    byear = dob.split("-")[0]
                    bmonth = dob.split("-")[1]
                    bday = dob.split("-")[2].split("T")[0]

                    prospect_id = helper.add_prospect(mlb_id, fname, lname, byear, bmonth, bday, p_type="professional")

                    try:
                        bats = info_info["bats"]
                        throws = info_info["throws"]
                        height = int(info_info["height_feet"])*12+int(info_info["height_inches"])
                        weight = int(info_info["weight"])                  
                    except UnicodeDecodeError:
                        bats, throws, height, weight = (None, None, None, None)
                    except ValueError:
                        print "\n\n**ERROR TAG** MLB_ERROR", str(year), str(mlb_id), str(fname), str(lname), "\n\n"
                        continue

                entry["prospect_id"] = prospect_id
                entry["bats"] = bats
                entry["throws"] = throws
                entry["height"] = height
                entry["weight"] = weight
                entry["birth_year"] = byear
                entry["birth_month"] = bmonth
                entry["birth_day"] = bday

                entry["team"] = player["team_file_code"]
                drafted = player_info["drafted"]                

                if list_type == "int":
                    drafted = None
                    try:
                        sign_text = player_info["signed"]
                        sign_value = sign_text.split(" - ")[1]
                        signed = sign_value
                    except IndexError:
                        signed = ""
                    try:
                        signed = int(signed.replace("$","").replace(",",""))
                    except ValueError:
                        signed = None

                    schoolcity = player_info["school"]
                    gradecountry = player_info["year"]
                    commit = None

                elif list_type == "draft":
                    try:
                        signed = player_info["preseason20"].replace(" ","").replace(",","").replace("$","").split("-")[1]
                    except (KeyError, IndexError):
                        signed = player_info["signed"].replace(" ","").replace(",","").replace("$","")
                    try:
                        signed = int(signed)
                    except ValueError:
                        signed = None
                    schoolcity = player_info["school"]
                    gradecountry = player_info["year"]
                    commit = player_info["signed"]
                else:
                    signed = player_info["signed"]
                    schoolcity = None
                    gradecountry = None
                    commit = None

                entry["drafted"] = drafted
                entry["signed"] = signed
                entry["school_city"] = schoolcity
                entry["grade_country"] = gradecountry
                entry["college_commit"] = commit

                if list_type not in ("int", "draft"):
                    eta = player_info["eta"]
                    try:
                        pre_top100 = player_info["preseason100"]
                    except KeyError:
                        pre_top100 = None
                else:
                    pre_top100 = None
                    eta = None

                entry["pre_top100"] = pre_top100
                entry["eta"] = eta

                entry["twitter"] = player_info["twitter"]

                blurb = player_info["content"]["default"].replace("<b>","").replace("</b>","").replace("<br />","").replace("<p>","").replace("</p>","").replace("*","")
                entry["blurb"] = blurb

                try:
                    overall_text = blurb.split("Overall")[1].split('\n')[0].replace(':','').replace(' ','')[:8]
                    if overall_text[0] not in (' ',':','0','1','2','3','4','5','6','7','8','9'):
                        raise IndexError

                    try:
                        text2 = overall_text.split('/')[1]
                    except IndexError:
                        text2 = overall_text.split('/')[-1]

                    overall = int(filter(str.isdigit, text2[:2]))
                except IndexError:
                    overall = 0

                if overall < 20 and overall is not None:
                    overall = overall*10
                entry["FV"] = overall

                entries.append(entry)

        if list_type == "draft":
            table = "mlb_prospects_draft"
        elif list_type == "int":
            table = "mlb_prospects_international"
        else:
            table = "mlb_prospects_professional"

        if entries != []:
            for i in range(0, len(entries), 1000):
                db.insertRowDict(entries[i: i + 1000], table, insertMany=True, replace=True, rid=0,debug=1)
                db.conn.commit()


if __name__ == "__main__":     
    parser = argparse.ArgumentParser()
    parser.add_argument("--end_year",type=int,default=2018)
    parser.add_argument("--scrape_length",type=str,default="Current")

    args = parser.parse_args()
    
    initiate(args.end_year, args.scrape_length)

