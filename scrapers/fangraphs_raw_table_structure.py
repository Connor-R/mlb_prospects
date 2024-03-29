from mechanize import Browser
import requests
from lxml import etree
from time import time, sleep, mktime
import argparse

from py_data_getter import data_getter
getter = data_getter()


br = Browser()
br.set_handle_robots(False)
br.set_handle_referer(False)
br.set_handle_refresh(False)
br.addheaders = [("User-agent", "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25"),
    ("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
    ("Keep-Alive","115"),
    ("Accept-Charset","ISO-8859-1,utf-8;q=0.7,*;q=0.7")
    ]

def initiate():
    keys = []
    for year in range(2015, 2023):
        if year >= 2018:
            keys = process_prospect_list(keys, year, "professional", "updated")
            sleep(5)
            
        for list_type, list_key in {"draft":"mlb","professional":"prospect","international":"int"}.items():

            if (
                (list_type=="professional" and year >= 2017) or 
                (list_type=="draft" and year >= 2015) or 
                (list_type=="international" and year >= 2015) or
                False
            ):

                keys = process_prospect_list(keys, year, list_type, list_key)
                sleep(5)




    qry = "DROP TABLE IF EXISTS `fg_raw`;\nCREATE TABLE `fg_raw` (\n`prospect_type` VARCHAR(64) NOT NULL DEFAULT '',"
    keys = list(set(keys))
    keys.sort()
    for k in keys:
        if str(k).upper() in ('PLAYERID', 'TEAM', 'TYPE', 'PLAYERNAME'):
            row_add = "\n`%s` VARCHAR(64) NOT NULL DEFAULT ''," % (str(k))
        else:
            row_add = "\n`%s` TEXT DEFAULT NULL," % (str(k))
        qry += row_add
        
    qry += "\nPRIMARY KEY (`prospect_type`, `PlayerId`,`Team`,`Type`,`playerName`)\n) ENGINE=InnoDB DEFAULT CHARSET=latin1;"

    print "\n\n\n\n\n", qry


def process_prospect_list(keys, year, list_type, list_key):
    url = "https://www.fangraphs.com/api/prospects/board/prospects-list?statType=player&draft=%s%s" % (year, list_key)
    print url

    json = getter.get_url_data(url, "json")

    for row in json:
        for tag in row:
            keys.append(tag)

    return keys


if __name__ == "__main__":     
    parser = argparse.ArgumentParser()

    args = parser.parse_args()
    
    initiate()

