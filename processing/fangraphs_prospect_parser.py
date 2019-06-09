from datetime import date, datetime, timedelta
import sys
from time import time, sleep, mktime
import argparse


from py_db import db
import prospect_helper as helper


db = db("mlb_prospects")

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

    col_names_query = """SELECT `COLUMN_NAME` 
    FROM `INFORMATION_SCHEMA`.`COLUMNS` 
    WHERE `TABLE_SCHEMA`='mlb_prospects' 
    AND `TABLE_NAME`='fg_raw';"""

    col_names = db.query(col_names_query)

    cols = []
    for cn in col_names:
        cols.append(cn[0])

    qry = """SELECT *
    FROM fg_raw
    WHERE 1
        AND season = %s
    ;"""

    query = qry % (year)

    res = db.query(query)

    row_val = {}
    for row in res:
        entry = {}
        for i, elt in enumerate(row):
            row_val[cols[i]] = elt

        p_type = row_val['prospect_type']
        fg_id = row_val['PlayerId']
        if fg_id in (0, ' '):
            fg_id = None
        fg_minor_id = row_val['minorMasterId']
        birth_date = row_val['BirthDate']
        age = row_val['Age']
        full_name = row_val['playerName']
        fname = row_val['FirstName']
        lname = row_val['LastName']

        full_name = full_name.replace("*","").replace(",", "").replace("  ", " ")
        fname = fname.replace("*", "")
        lname = lname.replace("*", "")

        full_name, fname2, lname2 = helper.adjust_fg_names(full_name)

        if fname2 is not None:
            fname = fname2
        if lname2 is not None:
            lname = lname2

        print year, p_type, fg_id, fg_minor_id, birth_date, age, full_name #####

        if birth_date is not None:
            try:
                date_object = datetime.strptime(birth_date, "%m/%d/%y")
            except ValueError:
                try:
                    date_object = datetime.strptime(birth_date, "%m/%d/%Y")
                except ValueError:
                    birth_date = None

        if birth_date is not None:
            bmonth, bday, byear = date_object.month, date_object.day, date_object.year
            est_years = byear

            if fg_id is not None:
                fg_id, byear, bmonth, bday = helper.adjust_fg_birthdays(fg_id, byear, bmonth, bday)
                if fg_id == fg_minor_id:
                    id_type = "fg_minor_id"
                else:
                    id_type = "fg_major_id"

                prospect_id = helper.add_prospect(fg_id, fname, lname, byear, bmonth, bday, "fg", id_type = id_type)
                if id_type == "fg_major_id" and fg_minor_id is not None:
                    foo = helper.add_prospect(fg_minor_id, fname, lname, byear, bmonth, bday, "fg", id_type = "fg_minor_id")

        elif age is not None:
            age = helper.adjust_fg_age(full_name, year, p_type, age)
            try:
                lower_year, upper_year = helper.est_fg_birthday(age, year, p_type)
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

            except (ValueError, TypeError):
                est_years = None
                prospect_id = 0

        else:
            prospect_id = 0
            est_years = None

        if fg_id is None:
            prospect_id = 0
            fg_id = str(full_name.replace(' ','')) + '_' + str(p_type) + '_' + str(year)
            print '\t\t\t\t', fg_id, birth_date
            # raw_input(prospect_id)

        entry['year'] = year
        entry['prospect_id'] = prospect_id
        entry['fg_id'] = fg_id
        entry['full_name'] = full_name
        entry['fname'] = fname
        entry['lname'] = lname
        entry['position'] = row_val['Position']
        entry['bats'] = row_val['Bats']
        entry['throws'] = row_val['Throws']
        entry['height'] = row_val['Height']
        entry['weight'] = row_val['Weight']
        entry['age'] = row_val['Age']
        entry['est_years'] = est_years
        entry['school'] = row_val['School']
        entry['athleticism'] = row_val['Athleticism']
        entry['performer'] = row_val['Performer']
        entry['risk'] = row_val['Risk_Current']
        entry['variance'] = row_val['Variance']
        entry['eta'] = row_val['ETA_Current']
        entry['fv'] = row_val['FV_Current']
        entry['video'] = row_val['YouTube']
        entry['short_blurb'] = row_val['TLDR']
        entry['blurb'] = row_val['Summary']

        if(0
            or (row_val['fCMD'] is not None and int(row_val['fCMD']) > 0)
            or (row_val['fFB'] is not None and int(row_val['fFB']) > 0)
            or (row_val['fCB'] is not None and int(row_val['fCB']) > 0)
            or (row_val['fCH'] is not None and int(row_val['fCH']) > 0)
            ):
            process_pitcher_grades(year, entry, row_val)

        if(0
            or (row_val['fHit'] is not None and int(row_val['fHit']) > 0)
            or (row_val['fGame'] is not None and int(row_val['fGame']) > 0)
            or (row_val['fSpd'] is not None and int(row_val['fSpd']) > 0)
            or (row_val['fFld'] is not None and int(row_val['fFld']) > 0)
            or (row_val['fArm'] is not None and int(row_val['fArm']) > 0)
            ):
            process_hitter_grades(year, entry, row_val)


        if p_type == 'draft':
            process_draft(year, entry, row_val)
        elif p_type == 'international':
            process_international(year, entry, row_val)
        elif p_type == 'professional':
            process_professional(year, entry, row_val)


def process_draft(year, entry, row_val):
    try:
        try:
            pick_num = int(row_val['Draft'].split('/')[0])
        except ValueError:
            pick_num = int(row_val['Draft'].split('/')[1])
        pick_team = row_val['Draft'].replace('/','').replace(str(pick_num),'')
    except (AttributeError, IndexError):
        pick_num, pick_team = None, None

    entry['college_commit'] = row_val['CollegeCommit']
    entry['draft_rank'] = ifzero(row_val['DraftRank'])
    entry['ovr_rank'] = ifzero(row_val['Ovr_Rank'])
    entry['pick_num'] = pick_num
    entry['pick_team'] = pick_team

    db.insertRowDict(entry, 'fg_prospects_draft', replace=True, debug=1)
    db.conn.commit()


def process_international(year, entry, row_val):
    entry['int_rank'] = ifzero(row_val['DraftRank'])

    db.insertRowDict(entry, 'fg_prospects_international', replace=True, debug=1)
    db.conn.commit()


def process_professional(year, entry, row_val):
    entry['level'] = ifzero(row_val['llevel']) #not sure difference between llevel and mlevel
    entry['org_rank'] = ifzero(row_val['Org_Rank'])
    entry['ovr_rank'] = ifzero(row_val['Ovr_Rank'])
    entry['signed'] = ifzero(row_val['Draft'])
    entry['team'] = ifzero(row_val['Team'])

    db.insertRowDict(entry, 'fg_prospects_professional', replace=True, debug=1)
    db.conn.commit()


def process_hitter_grades(year, entry, row_val):
    grade_entry = {}
    grade_entry['year'] = year
    grade_entry['fg_id'] = entry['fg_id']
    grade_entry['Hit_present'] = ifzero(row_val['pHit'])
    grade_entry['Hit_future'] = ifzero(row_val['fHit'])
    grade_entry['GamePower_present'] = ifzero(row_val['pGame'])
    grade_entry['GamePower_future'] = ifzero(row_val['fGame'])
    grade_entry['RawPower_present'] = ifzero(row_val['pRaw'])
    grade_entry['RawPower_future'] = ifzero(row_val['fRaw'])
    grade_entry['Speed_present'] = ifzero(row_val['pSpd'])
    grade_entry['Speed_future'] = ifzero(row_val['fSpd'])
    grade_entry['Field_present'] = ifzero(row_val['pFld'])
    grade_entry['Field_future'] = ifzero(row_val['fFld'])
    grade_entry['Throws_present'] = ifzero(row_val['pArm'])
    grade_entry['Throws_future'] = ifzero(row_val['fArm'])

    db.insertRowDict(grade_entry, 'fg_grades_hitters', replace=True, debug=1)
    db.conn.commit()

def process_pitcher_grades(year, entry, row_val):
    grade_entry = {}
    grade_entry['year'] = year
    grade_entry['fg_id'] = entry['fg_id']
    grade_entry['TJ_Date'] = ifzero(row_val['TJDate'])
    grade_entry['MaxVelo'] = ifzero(row_val['Vel'])
    grade_entry['Fastball_RPM'] = ifzero(row_val['fRPM'])
    grade_entry['Breaking_RPM'] = ifzero(row_val['bRPM'])
    grade_entry['Command_present'] = ifzero(row_val['pCMD'])
    grade_entry['Command_future'] = ifzero(row_val['fCMD'])
    grade_entry['Fastball_present'] = ifzero(row_val['pFB'])
    grade_entry['Fastball_future'] = ifzero(row_val['fFB'])
    grade_entry['Changeup_present'] = ifzero(row_val['pCH'])
    grade_entry['Changeup_future'] = ifzero(row_val['fCH'])
    grade_entry['Curveball_present'] = ifzero(row_val['pCB'])
    grade_entry['Curveball_future'] = ifzero(row_val['fCB'])
    grade_entry['Slider_present'] = ifzero(row_val['pSL'])
    grade_entry['Slider_future'] = ifzero(row_val['fSL'])
    grade_entry['Cutter_present'] = ifzero(row_val['pCT'])
    grade_entry['Cutter_future'] = ifzero(row_val['fCT'])
    grade_entry['Splitter_present'] = ifzero(row_val['pSPL'])
    grade_entry['Splitter_future'] = ifzero(row_val['fSPL'])

    db.insertRowDict(grade_entry, 'fg_grades_pitchers', replace=True, debug=1)
    db.conn.commit()


def ifzero(val):
    if val in (0, '0'):
        return None
    else:
        return val


if __name__ == "__main__":     
    parser = argparse.ArgumentParser()
    parser.add_argument("--end_year",type=int,default=2019)
    parser.add_argument("--scrape_length",type=str,default="All")

    args = parser.parse_args()
    
    initiate(args.end_year, args.scrape_length)