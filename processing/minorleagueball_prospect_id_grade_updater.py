import argparse
from time import time

import prospect_helper as helper
from py_db import db


db = db("mlb_prospects")


def initiate():
    start_time = time()

    clear_ids = "UPDATE minorleagueball_professional SET prospect_id = 0;"
    db.query(clear_ids)
    db.conn.commit()

    process_primary_update()
    process_secondary_update()

    end_time = time()
    elapsed_time = float(end_time - start_time)
    print "\n\nminorleagueball_prospect_id_grade_updater.py"
    print "time elapsed (in seconds): " + str(elapsed_time)
    print "time elapsed (in minutes): " + str(elapsed_time/60.0)


def process_primary_update():
    list_query = """SELECT year, prospect_id, team, fname, lname, age, grade
    FROM minorleagueball_professional p
    ORDER BY p.year ASC, p.team ASC, p.team_rank ASC;"""

    res = db.query(list_query)

    for row in res:
        year, prospect_id, team, fname, lname, age, grade = row

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


        grade_dict = {
            "A":65, "A/A-":63, "A-/A":62, "A-":60,
            "A-/B+":58, "B+/A-":56, "B+":55, "B+/B": 53, "B/B+": 52, "B":50, 
            "B/B-":48, "B-/B":46, "B-":45, "B-/C+": 43, "C+/B-": 42, "C+":40,
            "C+/C":38, "C/C+":36, "C":35}
        fv = grade_dict.get(grade)

        update_prospect(year, team, fname, lname, "prospect_id", prospect_id)
        update_prospect(year, team, fname, lname, "FV", fv)


def process_secondary_update():
    """
    Finds each player without a prospect id and matches them (via name/team) to a prospect +/- 1 year with a prospect id and then updates the id-less player.
    Iterates through until there are no players with a +/- 1 year match.
    """
    test = True
    while test == True:
        test_qry = """SELECT *
    FROM (SELECT *, YEAR AS 'yr' FROM minorleagueball_professional) p1
    JOIN (SELECT *, (YEAR-1) AS 'yr' FROM minorleagueball_professional) p2 USING (yr, team, fname, lname)
    WHERE p1.prospect_id != p2.prospect_id
    ORDER BY p1.year ASC, p1.team ASC, p1.team_rank ASC;"""
        test_val = db.query(test_qry)

        if test_val == ():
            test = False
        print(test)

        for yr in range(2013, 2019):
            qry = """SELECT 
        p1.team, p1.fname, p1.lname, 
        p1.year, p1.prospect_id,
        p2.year, p2.prospect_id
        FROM (SELECT *, YEAR AS 'yr' FROM minorleagueball_professional) p1
        JOIN (SELECT *, (YEAR-1) AS 'yr' FROM minorleagueball_professional) p2 USING (yr, team, fname, lname)
        WHERE p1.prospect_id != p2.prospect_id
        AND p1.year = %s
        ORDER BY p1.year ASC, p1.team ASC, p1.team_rank ASC;"""
            query = qry % (yr)
            res = db.query (query)

            for row in res:
                team, fname, lname, yr1, pid1, yr2, pid2 = row

                if pid1 == 0:
                    update_prospect(yr1, team, fname, lname, "prospect_id", pid2)
                elif pid2 == 0:
                    update_prospect(yr2, team, fname, lname, "prospect_id", pid1)
    

def update_prospect(year, team, fname, lname, category, value):

    print "\tupdate ", year, team, '\t', "{:<32}".format(fname+" "+lname), '\t', "{:<16}".format(category), '\t', value
    update_qry = """UPDATE minorleagueball_professional 
    SET %s = '%s'
    WHERE year = %s
    AND team = "%s"
    AND fname = "%s"
    AND lname = "%s";"""

    update_query = update_qry % (category, value, year, team, fname, lname)
    # raw_input(update_query)
    db.query(update_query)
    db.conn.commit()


if __name__ == "__main__":     
    parser = argparse.ArgumentParser()

    args = parser.parse_args()
    
    initiate()

