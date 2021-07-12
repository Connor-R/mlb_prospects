import argparse
from time import time
import sys
import tinyurl

from py_db import db

db = db("mlb_prospects")


def process():

    mlb_bat_url = 'https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=c,3,4,6,11,12,13,21,22,-1,34,35,40,-1,44,43,45,41,-1,23,37,38,50,61,-1,53,111,54,56,-1,315,316,317,305,306,307,308,309,310,311,-1,58&season=2021&month=0&season1=2021&ind=0&team=0&rost=0&age=0&filter=&players='

    mlb_pit_url = 'https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=c,3,4,5,11,7,8,13,-1,36,37,40,120,121,43,-1,44,48,51,-1,76,6,117,45,118,62,119,122,332,124,-1,322,323,324,325,326,327,328,331,-1,59&season=2021&month=0&season1=2021&ind=0&team=0&rost=0&age=0&filter=&players='

    all_bat_url = 'https://www.fangraphs.com/leaders/minor-league?pos=all&lg=2,4,5,6,7,8,9,10,11,14,12,13,15,16,17,18,30,32,33&stats=bat&qual=y&type=1&team=&season=2021&seasonEnd=2021&org=&ind=0&splitTeam=false&players='
    
    all_pit_url = 'https://www.fangraphs.com/leaders/minor-league/?pos=all&lg=2,4,5,6,7,8,9,10,11,14,12,13,15,16,17,18,30,32,33&stats=pit&qual=y&type=0&team=&season=2021&seasonEnd=2021&org=&ind=0&splitTeam=false&players='

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



    mlb_bat_url = mlb_bat_url[:-1] + '&sort=37,d&page=1_250'
    mlb_pit_url = mlb_pit_url[:-1] + '&sort=37,d&page=1_250'
    
    all_bat_url = all_bat_url[:-1] + '&sort=19,1&pageitems=10000000000000&pg=0'
    all_pit_url = all_pit_url[:-1] + '&sort=25,1&&pageitems=10000000000000&pg=0'

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
    