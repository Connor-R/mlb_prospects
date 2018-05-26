from datetime import date, datetime, timedelta
import sys
from time import time, sleep, mktime
import argparse
import csv
import os

import prospect_helper as helper
from py_db import db

db = db("mlb_prospects")


# We want to clear all entries for a given year so there aren't duplicates when we re-scrape (like if a fangraphs players gets a new player_id, there would be a duplicate)

def initiate(end_year, delete_length):
    start_time = time()

    if delete_length == 'All':
        for year in range (2013, end_year+1):
            process(year)
    else:
        year = end_year
        process(year)

    end_time = time()
    elapsed_time = float(end_time - start_time)
    print "\n\nprospect_db_rescrape_prep.py"
    print "time elapsed (in seconds): " + str(elapsed_time)
    print "time elapsed (in minutes): " + str(elapsed_time/60.0)


def process(delete_year):
    """
    Deleting the entries for a given year from the mlb_prospects tables and fg_prospects tables. 
    We leave the grades tablesas-is, since we want to keep duplicate records for grades.
    """

    print delete_year
    for table in ("mlb_prospects_international", "mlb_prospects_draft", "mlb_prospects_professional", "fg_prospects_international", "fg_prospects_draft", "fg_prospects_professional", "minorleagueball_professional"):

        print "\tDeleting", str(delete_year), "entries from", table

        delete_qry = "DELETE FROM %s WHERE year = %s;"

        delete_query = delete_qry % (table, delete_year)


        db.query(delete_query)
        db.conn.commit()


if __name__ == "__main__":     
    parser = argparse.ArgumentParser()
    parser.add_argument("--end_year",type=int,default=2018)
    parser.add_argument("--delete_length",type=str,default="Current")

    args = parser.parse_args()
    
    initiate(args.end_year, args.delete_length)


