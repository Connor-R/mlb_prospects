import sys
import argparse
from decimal import Decimal
from time import time

from py_db import db
db = db('mlb_prospects')

def initiate():
    start_time = time()

    process_hitters()
    process_pitchers()

    end_time = time()
    elapsed_time = float(end_time - start_time)
    print "\n\nprospect_grades.py"
    print "time elapsed (in seconds): " + str(elapsed_time)
    print "time elapsed (in minutes): " + str(elapsed_time/60.0)


def process_pitchers():
    entries = []
    query = """SELECT YEAR, mlb_id, _type, blurb 
    FROM(
        SELECT *, 'professional' AS '_type' FROM mlb_prospects_professional
        UNION ALL SELECT *, 'draft' AS '_type' FROM mlb_prospects_draft
        UNION ALL SELECT *, 'international' AS '_type' FROM mlb_prospects_international
    ) prospects
    WHERE LEFT(position,3) IN ('RHP','LHP','P')
    """
    res = db.query(query)    

    for row in res:
        entry = {}
        year, mlb_id, p_type, blurb = row

        print str(mlb_id) + ' (' + str(year) + ')',
        sys.stdout.flush()

        entry["year"] = year
        entry["mlb_id"] = mlb_id
        entry["prospect_type"] = p_type

        if mlb_id in (None, 0):
            continue

        if blurb[:4] == '\nPDP':
            continue

        try:
            try:
                control = int(blurb.split("Control")[1].split("|")[0].split('/')[-1].replace(':','').replace(' ','')[:8])
            except IndexError:
                control = int(blurb.split("Cont.")[1].split("|")[0].split('/')[-1].replace(':','').replace(' ','')[:8])
            except ValueError:
                control = int(blurb.split("Control")[1].split('\n')[0].split('/')[-1].replace(':','').replace(' ','')[:2])
        except IndexError:
            control = 0
        if control < 20 and control is not None:
            control = control*10
        entry["control"] = control


        try:
            fastball = int(blurb.split("Fastball")[1].split("|")[0].split('/')[-1].replace(':','').replace(' ','')[:8])
        except IndexError:
            try:
                fastball = int(blurb.split("FB")[1].split("|")[0].split('\n')[0].split('/')[-1].replace(':','').replace(' ','')[:8])
            except IndexError:
                fastball = None
        if fastball < 20 and fastball is not None:
            fastball = fastball*10
        entry["fastball"] = fastball


        try:
            change = int(blurb.split("Changeup")[1].split("|")[0].split('\n')[0].split('/')[-1].replace(':','').replace(' ','')[:8])
        except IndexError:
            try:
                change = int(blurb.split("Change")[1].split("|")[0].split('\n')[0].split('/')[-1].replace(':','').replace(' ','')[:8])
            except IndexError:
                change = None
        if change < 20 and change is not None:
            change = change*10
        entry["change"] = change


        try:
            curve = int(blurb.split("Curveball")[1].split("|")[0].split('\n')[0].split('/')[-1].replace(':','').replace(' ','')[:8])
        except IndexError:
            try:
                curve = int(blurb.split("Curve")[1].split("|")[0].split('\n')[0].split('/')[-1].replace(':','').replace(' ','')[:8])
            except IndexError:
                curve = None
        if curve < 20 and curve is not None:
            curve = curve*10
        entry["curve"] = curve


        try:
            slider = int(blurb.split("Slider")[1].split("|")[0].split('\n')[0].split('/')[-1].replace(':','').replace(' ','')[:8])
        except IndexError:
            slider = None
        if slider < 20 and slider is not None:
            slider = slider*10
        entry["slider"] = slider


        try:
            cutter = int(blurb.split("Cutter")[1].split("|")[0].split('\n')[0].split('/')[-1].replace(':','').replace(' ','')[:8])
        except IndexError:
            cutter = None
        if cutter < 20 and cutter is not None:
            cutter = cutter*10
        entry["cutter"] = cutter


        try:
            splitter = int(blurb.split("Splitter")[1].split("|")[0].split('\n')[0].split('/')[-1].replace(':','').replace(' ','')[:8])
        except IndexError:
            splitter = None
        if splitter < 20 and splitter is not None:
            splitter = splitter*10
        entry["splitter"] = splitter


        try:
            other = int(blurb.split("Screwball")[1].split("|")[0].split('\n')[0].split('/')[-1].replace(':','').replace(' ','')[:8])
        except IndexError:
            try:
                other = int(blurb.split("Knuckle")[1].split("|")[0].split('\n')[0].split('/')[-1].replace(':','').replace(' ','')[:8])
            except IndexError:
                try:
                    other = int(blurb.split("Palmball")[1].split("|")[0].split('\n')[0].split('/')[-1].replace(':','').replace(' ','')[:8])
                except IndexError:
                    other = None
        if other < 20 and other is not None:
            other = other*10
        entry["other"] = other

        entries.append(entry)

    if entries != []:
        for i in range(0, len(entries), 1000):
            db.insertRowDict(entries[i: i + 1000], 'mlb_grades_pitchers', insertMany=True, replace=True, rid=0,debug=1)
            db.conn.commit()


def process_hitters():
    entries = []
    query = """SELECT year, mlb_id, _type, blurb 
    FROM(
        SELECT *, 'professional' AS '_type' FROM mlb_prospects_professional
        UNION ALL SELECT *, 'draft' AS '_type' FROM mlb_prospects_draft
        UNION ALL SELECT *, 'international' AS '_type' FROM mlb_prospects_international
    ) prospects
    WHERE LEFT(position,3) NOT IN ('RHP','LHP','P')
    """
    res = db.query(query)

    for row in res:
        entry = {}
        year, mlb_id, p_type, blurb = row

        print str(mlb_id) + ' (' + str(year) + ')',
        sys.stdout.flush()

        entry["year"] = year
        entry["mlb_id"] = mlb_id
        entry["prospect_type"] = p_type

        if mlb_id in (None, 0):
            continue

        if blurb[:4] == '\nPDP':
            continue

        hit = int(blurb.split("Hit")[1].split("|")[0].split('\n')[0].split('/')[-1].replace(':','').replace(' ','')[:8])
        if hit < 20:
            hit = hit*10
        power = int(blurb.split("Power")[1].split("|")[0].split('\n')[0].split('/')[-1].replace(':','').replace(' ','')[:8])
        if power < 20:
            power = power*10
        try:
            run = int(blurb.split("Run")[1].split("|")[0].split('\n')[0].split('/')[-1].replace(':','').replace(' ','')[:8])
        except IndexError:
            run = int(blurb.split("Speed")[1].split("|")[0].split('\n')[0].split('/')[-1].replace(':','').replace(' ','')[:8])
        except ValueError:
            run = None
        if run < 20 and run > 0:
            run = run*10
        arm = int(blurb.split("Arm")[1].split("|")[0].split('\n')[0].split('/')[-1].replace(':','').replace(' ','')[:8])
        if arm < 20:
            arm = arm*10
        try:
            field = int(blurb.split("Field")[1].split("|")[0].split('\n')[0].split('/')[-1].replace(':','').replace(' ','')[:8])
        except IndexError:
            field = int(blurb.split("Defense")[1].split("|")[0].split('\n')[0].split('/')[-1].replace(':','').replace(' ','')[:8])
        except ValueError:
            field = int(blurb.split("Field")[1].split('\n')[0].split('/')[-1].replace(':','').replace(' ','')[:2])
        if field < 20:
            field = field*10

        entry["hit"] = hit
        entry["power"] = power
        entry["run"] = run
        entry["arm"] = arm
        entry["field"] = field

        entries.append(entry)

    if entries != []:
        for i in range(0, len(entries), 1000):
            db.insertRowDict(entries[i: i + 1000], 'mlb_grades_hitters', insertMany=True, replace=True, rid=0,debug=1)
            db.conn.commit()


if __name__ == "__main__":        
   
    initiate()
    