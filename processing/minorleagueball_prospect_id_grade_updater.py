import argparse
from time import time

import prospect_helper as helper
from py_db import db


db = db("mlb_prospects")


def initiate():
    start_time = time()

    process_primary_update()
    process_secondary_update()

    end_time = time()
    elapsed_time = float(end_time - start_time)
    print "\n\nprospect_grades.py"
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
    pass
    

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

