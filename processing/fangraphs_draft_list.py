import argparse
from time import time
import sys
import tinyurl

from py_db import db

db = db("mlb_prospects")


def process():

    mlb_bat_url = 'http://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=c,3,4,6,11,12,13,21,22,-1,34,35,40,-1,44,43,45,41,-1,23,37,38,50,61,-1,53,111,54,56,58&season=2019&month=0&ind=0&team=0&rost=0&age=0&filter=&players='

    mlb_pit_url = 'http://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=c,3,4,5,11,7,8,13,-1,36,37,40,120,121,43,-1,44,48,51,-1,76,6,117,45,118,62,119,122,124,-1,59&season=2019&month=0&season1=2017&ind=0&team=0&rost=0&age=0&filter=&players='

    all_bat_url = 'http://www.fangraphs.com/minorleaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=c,4,6,11,21,22,-1,24,25,30,32,-1,23,27,28,35,36,-1,31,33,34&season=2019&team=0&players='
    
    all_pit_url = 'http://www.fangraphs.com/minorleaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=c,4,5,11,7,8,12,23,-1,24,25,26,27,-1,28,29,36,-1,30,31,32,-1,40,52,-1,6,34,35,37,23&season=2019&team=0&players='


    get_players = """SELECT 
    p.mlb_id,
    p.fg_minor_id, 
    p.fg_major_id,
    position,
    CONCAT(COALESCE(p.mlb_fname, p.fg_fname), " ", COALESCE(p.mlb_lname, p.fg_lname)) as full_name
    FROM _draft_list d
    JOIN professional_prospects p USING (prospect_id);"""

    players = db.query(get_players)


    all_cnt = 0
    bat_cnt = 0
    pit_cnt = 0
    min_cnt = 0
    min_bat = 0
    min_pit = 0
    mlb_cnt = 0
    mlb_bat = 0
    mlb_pit = 0

    for player in players:
        mlb_id, fg_minor_id, fg_major_id, position, full_name = player

        if fg_minor_id is not None or fg_major_id is not None:
            all_cnt += 1
            if ("P" in position):
                pit_cnt += 1
                if fg_minor_id is not None:
                    min_cnt += 1
                    min_pit += 1
                    all_pit_url += str(fg_minor_id) + ','
                if fg_major_id is not None:
                    mlb_cnt += 1
                    mlb_pit += 1
                    mlb_pit_url += str(fg_major_id) + ','
            else:
                bat_cnt +=1
                if fg_minor_id is not None:
                    min_cnt += 1
                    min_bat += 1
                    all_bat_url += str(fg_minor_id) + ','
                if fg_major_id is not None:
                    mlb_cnt += 1
                    mlb_bat += 1
                    mlb_bat_url += str(fg_major_id) + ','



    mlb_bat_url = mlb_bat_url[:-1] + '&sort=27,d&page=1_250'
    mlb_pit_url = mlb_pit_url[:-1] + '&sort=28,d&page=1_250'
    
    all_bat_url = all_bat_url[:-1] + '&sort=19,d&page=1_250'
    all_pit_url = all_pit_url[:-1] + '&sort=26,d&page=1_250'

    cnt_state = """\nTotal Follows: \t\t\t%s \n\tBatter Follows: \t%s \n\tPitcher Follows: \t%s\n
    \nMLB Follows: \t\t\t%s \n\tMLB Hitters: \t\t%s \n\tMLB Pitchers: \t\t%s\n
    \nMiLB Follows: \t\t\t%s \n\tMiLB Hitters: \t\t%s \n\tMiLB Pitchers: \t\t%s\n 
    """ % (all_cnt, bat_cnt, pit_cnt, min_cnt, min_bat, min_pit, mlb_cnt, mlb_bat, mlb_pit)
    print cnt_state


    print '\n\tBatter Follows (major) URL: ' + str(mlb_bat) + ' players'
    print tinyurl.create_one(mlb_bat_url)

    print '\n\tBatter Follows (minor) URL: ' + str(min_bat) + ' players'
    print tinyurl.create_one(all_bat_url)

    print '\n\tPitcher Follows (major) URL: ' + str(mlb_pit) + ' players'
    print tinyurl.create_one(mlb_pit_url)

    print '\n\tPitcher Follows (minor)  URL: ' + str(min_pit) + ' players'
    print tinyurl.create_one(all_pit_url)

    print



if __name__ == "__main__":     
    process()
    