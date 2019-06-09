import requests
from mechanize import Browser
from time import time, sleep, mktime
import argparse
from lxml import etree

from py_data_getter import data_getter
from py_db import db
import prospect_helper as helper

db = db("mlb_prospects")
getter = data_getter()

sleep_time = 10
base_url = "https://www.fangraphs.com/api/prospects/board/prospects-list?statType=player&draft="

br = Browser()
br.set_handle_robots(False)
br.set_handle_referer(False)
br.set_handle_refresh(False)
br.addheaders = [("User-agent", "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25"),
    ("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
    ("Keep-Alive","115"),
    ("Accept-Charset","ISO-8859-1,utf-8;q=0.7,*;q=0.7")
    ]


start_time = time()

# run fangraphs_raw_table_structure.py first if you want to do a clean scrape

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
    for list_type, list_key in {"draft":"mlb","professional":"prospect","international":"int"}.items():

        if (
            (list_type=="professional" and year >= 2017) or 
            (list_type=="draft" and year >= 2015) or 
            (list_type=="international" and year >= 2015) or
            False
        ):

            process_prospect_list(year, list_type, list_key)

def process_prospect_list(year, list_type, list_key):

    list_url = base_url +"%s%s" % (year, list_key)
    print "\n", year, list_type, list_url

    data = br.open(list_url)
    tree = etree.parse(data)

    entries = []
    for plr in tree.iter('data'):
        entry = {'prospect_type':list_type}
        for p in plr.iter():

            key = p.tag
            val = p.text
            if type(val) in (str, unicode):
                val = "".join([i if ord(i) < 128 else "" for i in val])
            entry[key] = val
        
        print '\t', year, list_key, entry['playerName']
        db.insertRowDict(entry, 'fg_raw', insertMany=False, replace=True, rid=0,debug=1)
        db.conn.commit()
    sleep(sleep_time)


if __name__ == "__main__":     
    parser = argparse.ArgumentParser()
    parser.add_argument("--end_year",type=int,default=2019)
    parser.add_argument("--scrape_length",type=str,default="All")

    args = parser.parse_args()
    
    initiate(args.end_year, args.scrape_length)