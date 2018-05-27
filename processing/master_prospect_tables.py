import argparse
from time import time

from py_db import db


db = db("mlb_prospects")


def initiate():
    start_time = time()

    print "\ndeleteing _master_prospects"
    del_qry = """DROP TABLE IF EXISTS _master_prospects;"""
    del_query = del_qry
    db.query(del_query)
    db.conn.commit()

    query = "CREATE TABLE _master_prospects"
    for year in range(2013, 2019):
        query += process_prospects(year)
    query += ";"
    print "creating _master_prospects"
    db.query(query)
    db.conn.commit()

    end_time = time()
    elapsed_time = float(end_time - start_time)
    print "\n\nmaster_prospect_tables.py"
    print "time elapsed (in seconds): " + str(elapsed_time)
    print "time elapsed (in minutes): " + str(elapsed_time/60.0)


def process_prospects(year):

    print "\t", year

    if year == 2013:
        table_add = ""
    else:
        table_add = "UNION"

    table_qry = """%s 
    SELECT 
    %s as year,
    p.prospect_id, 
    p.mlb_id, 
    p.mlb_draft_id, 
    p.mlb_international_id, 
    p.fg_minor_id, 
    p.fg_major_id,
    "|" AS "*bio*",
    IF(p.fg_fname IS NULL, p.mlb_fname, p.fg_fname) AS first_name,
    IF(p.fg_lname IS NULL, p.mlb_lname, p.fg_lname) AS last_name,
    ROUND( DATEDIFF(STR_TO_DATE("%s-06-01", "%%Y-%%m-%%d"), STR_TO_DATE(CONCAT(p.birth_year,"-",p.birth_month,"-",p.birth_day), "%%Y-%%m-%%d"))/365.25, 2) AS age,
    COALESCE(fg.position, mlbp.position, mi.position, fgd.position, mlbd.position) AS position,
    COALESCE(mlbp.bats, fg.bats, mlbd.bats, fgd.bats, "unknown") AS bats,
    COALESCE(mlbp.throws, fg.throws, mlbd.throws, fgd.throws, "unknown") AS throws,
    COALESCE(mlbp.height, fg.height, mlbd.height, fgd.height, "unknown") AS height,
    COALESCE(mlbp.weight, fg.weight, mlbd.weight, fgd.weight, "unknown") AS weight,
    IF(fgd.rank IS NULL AND mlbd.rank IS NULL, "professional", "draft") AS p_type,
    ( 4*IFNULL(fg.FV,0) + 3*IFNULL(mi.FV,0) + 2*IFNULL(mlbp.FV,0) + 3*IFNULL(fgd.FV,0) + 1*IFNULL(mlbd.FV,0) ) 
    as "FV_pts",
    ROUND(
    ( 4*IFNULL(fg.FV/fg.FV,0) + 3*IFNULL(mi.FV/mi.FV,0) + 2*IFNULL(mlbp.FV/mlbp.FV,0) + 3*IFNULL(fgd.FV/fgd.FV,0) + 1*IFNULL(mlbd.FV/mlbd.FV,0) )
    , 0 ) as "FV_weight",
    ROUND( 
    ( 4*IFNULL(fg.FV,0) + 3*IFNULL(mi.FV,0) + 2*IFNULL(mlbp.FV,0) + 3*IFNULL(fgd.FV,0) + 1*IFNULL(mlbd.FV,0) )
        /
    ( 4*IFNULL(fg.FV/fg.FV,0) + 3*IFNULL(mi.FV/mi.FV,0) + 2*IFNULL(mlbp.FV/mlbp.FV,0) + 3*IFNULL(fgd.FV/fgd.FV,0) + 1*IFNULL(mlbd.FV/mlbd.FV,0) ) 
    , 1) AS "avg_FV",
    "|" AS "*fg*",
    fg.top100 AS fg100,
    fg.team AS fg_team,
    fg.team_rank AS fg_teamRank,
    fg.position AS fg_position,
    fg.signed AS fg_signed,
    fg.signed_from AS fg_signedFrom,
    fg.eta AS fg_eta,
    fg.FV AS fg_FV,
    "|" AS "*mi*",
    mi.team AS mi_team,
    mi.team_rank AS mi_teamRank,
    mi.grade AS mi_grade,
    mi.FV AS mi_FV,
    "|" AS "*mlb*",
    mlbp.pre_top100 AS mlbp_top100,
    mlbp.team AS mlbp_team,
    mlbp.drafted AS mlbp_drafted,
    mlbp.signed AS mlbp_signed,
    mlbp.eta AS mlbp_eta,
    mlbp.FV AS mlbp_FV,
    "|" AS "*fg_draft*",
    fgd.rank AS fgd_rank,
    fgd.school AS fgd_school,
    fgd.FV AS fgd_FV,
    "|" AS "*mlb_draft*",
    mlbd.rank AS mlbd_rank,
    mlbd.school_city AS mlbd_school,
    mlbd.grade_country AS mlbd_grade,
    mlbd.FV AS mlbd_FV,
    "|" AS "*extras*",
    fg.video AS fg_video,
    mi.blurb AS mi_blurb,
    mlbp.blurb AS mlbp_blurb,
    fgd.video AS fgd_video,
    fgd.blurb AS fgd_blurb,
    mlbd.blurb AS mlbd_blurb
    FROM (SELECT *, %s AS YEAR FROM professional_prospects) p
    LEFT JOIN fg_prospects_professional fg USING (YEAR, prospect_id)
    LEFT JOIN minorleagueball_professional mi USING (YEAR, prospect_id)
    LEFT JOIN mlb_prospects_professional mlbp USING (YEAR, prospect_id)
    LEFT JOIN fg_prospects_draft fgd USING (YEAR, prospect_id)
    LEFT JOIN mlb_prospects_draft mlbd USING (YEAR, prospect_id)
    WHERE (fg.year IS NOT NULL OR mi.year IS NOT NULL OR mlbp.year IS NOT NULL OR fgd.year IS NOT NULL OR mlbd.year IS NOT NULL)"""

    table_query = table_qry % (table_add, year, year, year)

    return table_query


if __name__ == "__main__":     
    parser = argparse.ArgumentParser()

    args = parser.parse_args()
    
    initiate()

