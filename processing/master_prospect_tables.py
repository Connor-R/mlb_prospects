import argparse
from time import time
import csv
from xlsxwriter.workbook import Workbook
import os

from py_db import db
db = db("mlb_prospects")

year = 2018

def initiate():
    start_time = time()

    print "\n\ndeleteing _master_prospects"
    del_qry = """DROP TABLE IF EXISTS _master_prospects;"""
    del_query = del_qry
    db.query(del_query)
    db.conn.commit()

    print "\ncreating _master_prospects"
    query = "CREATE TABLE _master_prospects"
    for yr in range(2013, year+1):
        query += process_prospects(yr)
    print "writing _master_prospects"
    query += ";"
    db.query(query)
    db.conn.commit()

    print "\nupdating tables"
    update_tables(year)


    print "\nexporting to .xlsx"
    export_tables(year)

    print "\nexporting master to .csv"
    export_masterCSV("_master_prospects")


    end_time = time()
    elapsed_time = float(end_time - start_time)
    print "\n\nmaster_prospect_tables.py"
    print "time elapsed (in seconds): " + str(elapsed_time)
    print "time elapsed (in minutes): " + str(elapsed_time/60.0)


def process_prospects(year):

    print "\t getting prospects from ", year

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
    COALESCE(fg.position, fgd.position, mlbp.position, mlbd.position, mi.position) AS position,
    COALESCE(mlbp.bats, fg.bats, mlbd.bats, fgd.bats, "unknown") AS bats,
    COALESCE(mlbp.throws, fg.throws, mlbd.throws, fgd.throws, "unknown") AS throws,
    COALESCE(mlbp.height, fg.height, mlbd.height, fgd.height, "unknown") AS height,
    COALESCE(mlbp.weight, fg.weight, mlbd.weight, fgd.weight, "unknown") AS weight,
    IF(fgd.rank IS NULL AND mlbd.rank IS NULL, "professional", "draft") AS p_type,
    ( 4*IFNULL(fg.FV,0) + 3*IFNULL(mi.FV,0) + 2*IFNULL((mlbp.FV-5),0) + 3*IFNULL(fgd.FV,0) + 1*IFNULL((mlbd.FV-5),0) ) 
    as "FV_pts",
    ROUND(
    ( 4*IFNULL(fg.FV/fg.FV,0) + 3*IFNULL(mi.FV/mi.FV,0) + 2*IFNULL(mlbp.FV/mlbp.FV,0) + 3*IFNULL(fgd.FV/fgd.FV,0) + 1*IFNULL(mlbd.FV/mlbd.FV,0) )
    , 0 ) as "FV_weight",
    ROUND( 
    ( 4*IFNULL(fg.FV,0) + 3*IFNULL(mi.FV,0) + 2*IFNULL((mlbp.FV-5),0) + 3*IFNULL(fgd.FV,0) + 1*IFNULL((mlbd.FV-5),0) ) 
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
    mi.eta as mi_eta,
    mi.FV AS mi_FV,
    "|" AS "*mlb*",
    mlbp.pre_top100 AS mlbp_top100,
    mlbp.team AS mlbp_team,
    mlbp.drafted AS mlbp_drafted,
    mlbp.signed AS mlbp_signed,
    mlbp.eta AS mlbp_eta,
    mlbp.FV AS mlbp_FV,
    "|" AS "*fg_draft*",
    fgd.top100 AS fgd_top100,
    fgd.rank AS fgd_rank,
    fgd.pick_team as fgd_pick_team,
    fgd.pick_num as fgd_pick_num,
    fgd.school AS fgd_school,
    fgd.college_commit AS fgd_college_commit,
    fgd.athleticism as fg_athleticiscm,
    fgd.frame as fg_frame,
    fgd.performance as fg_performance,
    fgd.risk AS fgd_risk,
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
    mlbd.blurb AS mlbd_blurb,
    "|" AS "*ofp*",
    ROUND( (3*fgh.Hit_present + fgh.GamePower_present + RawPower_present + Field_present + Speed_present)/7.00, 1) AS fg_hit_OFP_present,
    ROUND( (3*fgh.Hit_future + fgh.GamePower_future + RawPower_future + Field_future + Speed_future)/7.00, 1) AS fg_hit_OFP_future,
    ROUND( 
        (IFNULL(fgp.Fastball_present, 0) + IFNULL(fgp.Changeup_present, 0) + 
        IFNULL(fgp.Curveball_present, 0) + IFNULL(fgp.Slider_present, 0) +
        IFNULL(fgp.Cutter_present, 0) + IFNULL(fgp.Splitter_present, 0) +
        IFNULL(fgp.Other_present, 0) + 3*IFNULL(fgp.Command_present, 0)
        )/
        (IFNULL(fgp.Fastball_present/fgp.Fastball_present, 0) + IFNULL(fgp.Changeup_present/fgp.Changeup_present, 0) + 
        IFNULL(fgp.Curveball_present/fgp.Curveball_present, 0) + IFNULL(fgp.Slider_present/fgp.Slider_present, 0) +
        IFNULL(fgp.Cutter_present/fgp.Cutter_present, 0) + IFNULL(fgp.Splitter_present/fgp.Splitter_present, 0) +
        IFNULL(fgp.Other_present/fgp.Other_present, 0) + 3*IFNULL(fgp.Command_present/fgp.Command_present, 0)
        )
    , 1) AS fg_pit_OFP_present,
    ROUND( 
        (IFNULL(fgp.Fastball_future, 0) + IFNULL(fgp.Changeup_future, 0) + 
        IFNULL(fgp.Curveball_future, 0) + IFNULL(fgp.Slider_future, 0) +
        IFNULL(fgp.Cutter_future, 0) + IFNULL(fgp.Splitter_future, 0) +
        IFNULL(fgp.Other_future, 0) + 3*IFNULL(fgp.Command_future, 0)
        )/
        (IFNULL(fgp.Fastball_future/fgp.Fastball_future, 0) + IFNULL(fgp.Changeup_future/fgp.Changeup_future, 0) + 
        IFNULL(fgp.Curveball_future/fgp.Curveball_future, 0) + IFNULL(fgp.Slider_future/fgp.Slider_future, 0) +
        IFNULL(fgp.Cutter_future/fgp.Cutter_future, 0) + IFNULL(fgp.Splitter_future/fgp.Splitter_future, 0) +
        IFNULL(fgp.Other_future/fgp.Other_future, 0) + 3*IFNULL(fgp.Command_future/fgp.Command_future, 0)
        )
    , 1) AS fg_pit_OFP_future,
    ROUND( -2.5 + (3*mgh.hit + 2*mgh.power + mgh.field + mgh.run)/7.00, 1) AS mlb_hit_OFP,
    ROUND( -5.0 +
        (IFNULL(mgp.fastball, 0) + IFNULL(mgp.change, 0) + 
        IFNULL(mgp.curve, 0) + IFNULL(mgp.slider, 0) +
        IFNULL(mgp.cutter, 0) + IFNULL(mgp.splitter, 0) +
        IFNULL(mgp.other, 0) + 3*IFNULL(mgp.control, 0)
        )/
        (IFNULL(mgp.fastball/mgp.fastball, 0) + IFNULL(mgp.change/mgp.change, 0) + 
        IFNULL(mgp.curve/mgp.curve, 0) + IFNULL(mgp.slider/mgp.slider, 0) +
        IFNULL(mgp.cutter/mgp.cutter, 0) + IFNULL(mgp.splitter/mgp.splitter, 0) +
        IFNULL(mgp.other/mgp.other, 0) + 3*IFNULL(mgp.control/mgp.control, 0)
        )
    , 1) AS mlb_pit_OFP,
    "|" AS "*flags*",
    IF((
     mi.blurb LIKE "%%sleeper%%" OR mi.blurb LIKE "%%attention%%" OR mi.blurb LIKE "%%notice%%" OR mi.blurb LIKE "%% raves %%" OR mi.blurb LIKE "%%glowing%%" OR mi.blurb LIKE "%%undderrated%%" 
     OR 
     mlbp.blurb LIKE "%%sleeper%%" OR mlbp.blurb LIKE "%%attention%%" OR mlbp.blurb LIKE "%%notice%%" OR mlbp.blurb LIKE "%% raves %%" OR mlbp.blurb LIKE "%%glowing%%" OR mlbp.blurb LIKE "%%undderrated%%" 
     OR
     fgd.blurb LIKE "%%sleeper%%" OR fgd.blurb LIKE "%%attention%%" OR fgd.blurb LIKE "%%notice%%" OR fgd.blurb LIKE "%% raves %%" OR fgd.blurb LIKE "%%glowing%%" OR fgd.blurb LIKE "%%undderrated%%" 
     OR
     mlbd.blurb LIKE "%%sleeper%%" OR mlbd.blurb LIKE "%%attention%%" OR mlbd.blurb LIKE "%%notice%%" OR mlbd.blurb LIKE "%% raves %%" OR mlbd.blurb LIKE "%%glowing%%" OR mlbd.blurb LIKE "%%undderrated%%" 
     )
    , 1, 0) AS "sleeper",
    IF((
     mi.blurb LIKE "%%buzz%%" OR mi.blurb LIKE "%%breakout%%" OR mi.blurb LIKE "%%breakthrough%%" OR mi.blurb LIKE "%%leap%%" OR mi.blurb LIKE "%%promising%%" 
     OR 
     mlbp.blurb LIKE "%%buzz%%" OR mlbp.blurb LIKE "%%breakout%%" OR mlbp.blurb LIKE "%%breakthrough%%" OR mlbp.blurb LIKE "%%leap%%" OR mlbp.blurb LIKE "%%promising%%" 
     OR
     fgd.blurb LIKE "%%buzz%%" OR fgd.blurb LIKE "%%breakout%%" OR fgd.blurb LIKE "%%breakthrough%%" OR fgd.blurb LIKE "%%leap%%" OR fgd.blurb LIKE "%%promising%%" 
     OR
     mlbd.blurb LIKE "%%buzz%%" OR mlbd.blurb LIKE "%%breakout%%" OR mlbd.blurb LIKE "%%breakthrough%%" OR mlbd.blurb LIKE "%%leap%%" OR mlbd.blurb LIKE "%%promising%%" 
     )
    , 1, 0) AS "breakout",
    IF((
     mi.blurb LIKE "%%top-of-the-rotation%%" OR mi.blurb LIKE "%%top of the rotation%%" OR mi.blurb LIKE "%%upside%%" OR mi.blurb LIKE "%%high ceiling%%" OR mi.blurb LIKE "%%high risk%%" 
     OR 
     mlbp.blurb LIKE "%%top-of-the-rotation%%" OR mlbp.blurb LIKE "%%top of the rotation%%" OR mlbp.blurb LIKE "%%upside%%" OR mlbp.blurb LIKE "%%high ceiling%%" OR mlbp.blurb LIKE "%%high risk%%" 
     OR
     fgd.blurb LIKE "%%top-of-the-rotation%%" OR fgd.blurb LIKE "%%top of the rotation%%" OR fgd.blurb LIKE "%%upside%%" OR fgd.blurb LIKE "%%high ceiling%%" OR fgd.blurb LIKE "%%high risk%%" 
     OR
     mlbd.blurb LIKE "%%top-of-the-rotation%%" OR mlbd.blurb LIKE "%%top of the rotation%%" OR mlbd.blurb LIKE "%%upside%%" OR mlbd.blurb LIKE "%%high ceiling%%" OR mlbd.blurb LIKE "%%high risk%%" 
     )
    , 1, 0) AS "upside",
    IF((
     mi.blurb LIKE "%%excellent command%%" OR mi.blurb LIKE "%%young for%%" OR mi.blurb LIKE "%%could advance%%" OR mi.blurb LIKE "%%athleticg%%" OR mi.blurb LIKE "%%exciting%%" 
     OR 
     mlbp.blurb LIKE "%%excellent command%%" OR mlbp.blurb LIKE "%%young for%%" OR mlbp.blurb LIKE "%%could advance%%" OR mlbp.blurb LIKE "%%athletic%%" OR mlbp.blurb LIKE "%%exciting%%" 
     OR
     fgd.blurb LIKE "%%excellent command%%" OR fgd.blurb LIKE "%%young for%%" OR fgd.blurb LIKE "%%could advance%%" OR fgd.blurb LIKE "%%athletic%%" OR fgd.blurb LIKE "%%exciting%%" 
     OR
     mlbd.blurb LIKE "%%excellent command%%" OR mlbd.blurb LIKE "%%young for%%" OR mlbd.blurb LIKE "%%could advance%%" OR mlbd.blurb LIKE "%%athletic%%" OR mlbd.blurb LIKE "%%exciting%%" 
     )
    , 1, 0) AS "personal_traits",
    "|" AS "*fg hit*",
    fgh.Hit_present, fgh.GamePower_present, fgh.RawPower_present, fgh.Speed_present, fgh.Field_present, fgh.Throws_present,
    fgh.Hit_future, fgh.GamePower_future, fgh.RawPower_future, fgh.Speed_future, fgh.Field_future, fgh.Throws_future,
    "|" AS "*fh pit*",
    fgp.Fastball_present, fgp.Changeup_present, fgp.Curveball_present, fgp.Slider_present, fgp.Cutter_present, fgp.Splitter_present, fgp.Other_present, fgp.Command_present, 
    fgp.Fastball_future, fgp.Changeup_future, fgp.Curveball_future, fgp.Slider_future, fgp.Cutter_future, fgp.Splitter_future, fgp.Other_future, fgp.Command_future,
    "|" AS "*mlb hit*",
    mgh.hit, mgh.power, mgh.run, mgh.arm, mgh.field,
    "|" AS "*mlb pit*",
    mgp.fastball, mgp.change, mgp.curve, mgp.slider, mgp.cutter, mgp.splitter, mgp.other, mgp.control    
    FROM (SELECT *, %s AS YEAR FROM professional_prospects) p
    LEFT JOIN fg_prospects_professional fg USING (YEAR, prospect_id)
    LEFT JOIN minorleagueball_professional mi USING (YEAR, prospect_id)
    LEFT JOIN mlb_prospects_professional mlbp USING (YEAR, prospect_id)
    LEFT JOIN fg_prospects_draft fgd USING (YEAR, prospect_id)
    LEFT JOIN mlb_prospects_draft mlbd USING (YEAR, prospect_id)
    LEFT JOIN fg_grades_hitters fgh ON (p.year = fgh.year AND (p.fg_minor_id = fgh.fg_id OR p.fg_major_id = fgh.fg_id))
    LEFT JOIN fg_grades_pitchers fgp ON (p.year = fgp.year AND (p.fg_minor_id = fgp.fg_id OR p.fg_major_id = fgp.fg_id))
    LEFT JOIN mlb_grades_hitters mgh ON (p.year = mgh.year AND (CONVERT(p.mlb_id,CHAR) = mgh.mlb_id OR p.mlb_draft_id = mgh.mlb_id OR p.mlb_international_id = mgh.mlb_id))
    LEFT JOIN mlb_grades_pitchers mgp ON (p.year = mgp.year AND (CONVERT(p.mlb_id,CHAR) = mgp.mlb_id OR p.mlb_draft_id = mgp.mlb_id OR p.mlb_international_id = mgp.mlb_id))
    WHERE (fg.year IS NOT NULL OR mi.year IS NOT NULL OR mlbp.year IS NOT NULL OR fgd.year IS NOT NULL OR mlbd.year IS NOT NULL)"""

    table_query = table_qry % (table_add, year, year, year)

    return table_query


def update_tables(year):
    qry = """
    # create semi-temporary master table
    SET @cur_year = %s;
    DROP TABLE IF EXISTS _master_current_temp;
    CREATE TABLE _master_current_temp
    SELECT
    first_name,
    last_name,
    m.age, m.position, m.bats, m.throws, m.p_type,
    COALESCE(m.mlbp_team, m.fgd_pick_team, m.mlbd_school, m.fg_team, m.mi_team) AS "cur_team",
    "|" AS "*overall*",
    ROUND(
    ( 5*m.avg_FV +
    0.25*IFNULL(COALESCE(m.fg_pit_OFP_present, m.fg_hit_OFP_present), 0) + 
    1.25*IFNULL(COALESCE(m.fg_pit_OFP_future, m.fg_hit_OFP_future), 0) + 
    0.50*IFNULL(COALESCE(m.mlb_pit_OFP, m.mlb_hit_OFP), 0) 
    ) /
    (5 + 
    0.25*IFNULL((COALESCE(m.fg_pit_OFP_present, m.fg_hit_OFP_present)/COALESCE(m.fg_pit_OFP_present, m.fg_hit_OFP_present)), 0) + 
    1.25*IFNULL((COALESCE(m.fg_pit_OFP_future, m.fg_hit_OFP_future)/COALESCE(m.fg_pit_OFP_future, m.fg_hit_OFP_future)), 0) + 
    0.50*IFNULL((COALESCE(m.mlb_pit_OFP, m.mlb_hit_OFP)/COALESCE(m.mlb_pit_OFP, m.mlb_hit_OFP)), 0) 
    )
    + IFNULL(shortlist_value, 0) 
    + ((m.sleeper + m.breakout + m.upside + m.personal_traits)/4)
    , 1) AS superAdj_FV,
    ROUND(
    ( 5*m.avg_FV +
    0.25*IFNULL(COALESCE(m.fg_pit_OFP_present, m.fg_hit_OFP_present), 0) + 
    1.25*IFNULL(COALESCE(m.fg_pit_OFP_future, m.fg_hit_OFP_future), 0) + 
    0.50*IFNULL(COALESCE(m.mlb_pit_OFP, m.mlb_hit_OFP), 0) 
    ) /
    (5 + 
    0.25*IFNULL((COALESCE(m.fg_pit_OFP_present, m.fg_hit_OFP_present)/COALESCE(m.fg_pit_OFP_present, m.fg_hit_OFP_present)), 0) + 
    1.25*IFNULL((COALESCE(m.fg_pit_OFP_future, m.fg_hit_OFP_future)/COALESCE(m.fg_pit_OFP_future, m.fg_hit_OFP_future)), 0) + 
    0.50*IFNULL((COALESCE(m.mlb_pit_OFP, m.mlb_hit_OFP)/COALESCE(m.mlb_pit_OFP, m.mlb_hit_OFP)), 0) 
    )
    , 1) AS adj_FV,
    m.avg_FV AS avg_FV,
    ROUND(
    (0.25*IFNULL(COALESCE(m.fg_pit_OFP_present, m.fg_hit_OFP_present), 0) + 
    2.75*IFNULL(COALESCE(m.fg_pit_OFP_future, m.fg_hit_OFP_future), 0) + 
    1.00*IFNULL(COALESCE(m.mlb_pit_OFP, m.mlb_hit_OFP), 0) 
    ) /
    (
    0.25*IFNULL((COALESCE(m.fg_pit_OFP_present, m.fg_hit_OFP_present)/COALESCE(m.fg_pit_OFP_present, m.fg_hit_OFP_present)), 0) + 
    2.75*IFNULL((COALESCE(m.fg_pit_OFP_future, m.fg_hit_OFP_future)/COALESCE(m.fg_pit_OFP_future, m.fg_hit_OFP_future)), 0) + 
    1.00*IFNULL((COALESCE(m.mlb_pit_OFP, m.mlb_hit_OFP)/COALESCE(m.mlb_pit_OFP, m.mlb_hit_OFP)), 0) 
    )
    , 1) AS ofp_FV,
    ROUND((m.sleeper + m.breakout + m.upside + m.personal_traits)/4,2) AS flag_value,
    s.shortlist_value,
    s.shortlist_notes,
    "|" AS "*FV*",
    m.FV_pts, 
    m.fg_FV, m.mi_grade, m.mlbp_FV, m.fgd_FV, m.mlbd_FV,
    COALESCE(m.fg_pit_OFP_present, m.fg_hit_OFP_present) AS fg_OFP_present,
    COALESCE(m.fg_pit_OFP_future, m.fg_hit_OFP_future) AS fg_OFP_future,
    COALESCE(m.mlb_pit_OFP, m.mlb_hit_OFP) AS mlb_OFP,
    "|" AS "*flags*", m.sleeper, m.breakout, m.upside, m.personal_traits,
    "|" AS "*rnk*", m.fg100, m.mlbp_top100, m.fgd_top100, m.fgd_rank, m.mlbd_rank,
    "|" AS "*eta*", m.fg_eta, m.mi_eta, m.mlbp_eta,
    "|" AS "*intang*", m.fg_athleticiscm, m.fg_frame, m.fg_performance,
    "|" AS "*extras*", m.mi_blurb, mlbp_blurb, fgd_blurb, mlbd_blurb, fg_video, fgd_video,
    "|" AS "*bio*", m.prospect_id, m.height, m.weight, 
    "|" AS "*team*", m.fg_team, m.mi_team, m.mlbp_team, m.fgd_pick_team, m.fgd_pick_num, m.fg_signed, m.fg_signedFrom, m.mlbp_signed, 
    "|" AS "*edu*", m.fgd_school, m.fgd_college_commit, m.mlbd_school, m.mlbd_grade,
    "|" AS "*nsbl*", cr.team_abb AS "NSBL_team", cr.salary, cr.year AS "contract",
    "|" AS "*fg hit*",
    m.Hit_present, m.GamePower_present, m.RawPower_present, m.Speed_present, m.Field_present, m.Throws_present,
    m.Hit_future, m.GamePower_future, m.RawPower_future, m.Speed_future, m.Field_future, m.Throws_future,
    "|" AS "*fh pit*",
    m.Fastball_present, m.Changeup_present, m.Curveball_present, m.Slider_present, m.Cutter_present, m.Splitter_present, m.Other_present, m.Command_present, 
    m.Fastball_future, m.Changeup_future, m.Curveball_future, m.Slider_future, m.Cutter_future, m.Splitter_future, m.Other_future, m.Command_future,
    "|" AS "*mlb hit*",
    m.hit, m.power, m.run, m.arm, m.field,
    "|" AS "*mlb pit*",
    m.fastball, m.change, m.curve, m.slider, m.cutter, m.splitter, m.other, m.control
    FROM _master_prospects m
    LEFT JOIN NSBL.current_rosters_excel cr ON (cr.player_name LIKE CONCAT(m.first_name, "%%") AND cr.player_name LIKE CONCAT("%%", m.last_name))
    LEFT JOIN _shortlisted s USING (first_name, last_name)
    WHERE m.year = @cur_year
    ORDER BY superAdj_FV DESC, adj_FV DESC, avg_FV DESC, FV_pts DESC, FV_weight DESC, age ASC
    ;
    # create semi-temporary rank table
    DROP TABLE IF EXISTS _master_current_temp_rank;
    SET @rowno1 = 0; 
    SET @rowno2 = 0; 
    SET @rowno3 = 0; 
    SET @rowno4 = 0; 
    CREATE TABLE _master_current_temp_rank 
    SELECT 
    *
    FROM(
        SELECT
        @rowno1:=@rowno1+1 AS `superAdj_rnk`,
        first_name, last_name, age FROM (SELECT first_name, last_name, age, superAdj_FV, adj_FV, avg_FV, ofp_FV FROM _master_current_temp mc
        ORDER BY superAdj_FV DESC ) a1
    ) a2
    JOIN(
        SELECT
        @rowno2:=@rowno2+1 AS `adj_rnk`,
        first_name, last_name, age FROM (SELECT first_name, last_name, age, superAdj_FV, adj_FV, avg_FV, ofp_FV FROM _master_current_temp mc 
        ORDER BY adj_FV DESC ) b1 
    ) b2 USING (first_name, last_name, age)
    JOIN(
        SELECT
        @rowno3:=@rowno3+1 AS `avg_rnk`,
        first_name, last_name, age FROM (SELECT first_name, last_name, age, superAdj_FV, adj_FV, avg_FV, ofp_FV FROM _master_current_temp mc
        ORDER BY avg_FV DESC ) c1 
    ) c2 USING (first_name, last_name, age)
    JOIN(
        SELECT
        @rowno4:=@rowno4+1 AS `ofp_rnk`,
        first_name, last_name, age FROM( SELECT first_name, last_name, age, superAdj_FV, adj_FV, avg_FV, ofp_FV FROM _master_current_temp mc
        ORDER BY ofp_FV DESC ) d1
    ) d2 USING (first_name, last_name, age)
    ;

    # current year pref list
    DROP TABLE IF EXISTS _master_current;
    SET @rowno = 0; 
    CREATE TABLE _master_current 
    SELECT
    mcr.superAdj_rnk, mcr.adj_rnk, mcr.avg_rnk, mcr.ofp_rnk,
    "|" AS "*data*",
    mc.*
    FROM _master_current_temp mc
    JOIN _master_current_temp_rank mcr USING (first_name, last_name, age)
    ;


    # draft pref list
    DROP TABLE IF EXISTS _draft_list;
    SET @rowno = 0; 
    CREATE TABLE _draft_list 
    SELECT
    @rowno:=@rowno+1 AS `draft_rnk`,
    a.*
    FROM(
        SELECT
        *
        FROM _master_current mc
        WHERE NSBL_team IS NULL
        AND CONCAT(first_name," ",last_name) NOT IN ("Shohei Ohtani","Julio Pablo Martinez","Luis Robert","Alexander Canario","Wander Franco", "Ronny Mauricio", "Kristian Robinson")
        ORDER BY mc.superAdj_FV DESC, mc.adj_FV DESC, mc.avg_FV DESC, mc.ofp_FV DESC
    ) a
    ; 

    # Delete semi-temporary tables
    DROP TABLE IF EXISTS _master_current_temp;
    DROP TABLE IF EXISTS _master_current_temp_rank;
    """

    query_full = qry % (year)
    # raw_input(query_full)

    for query in query_full.split(";")[:-1]:
        db.query(query)


def export_tables(year):
    for table_name in ("_draft_list", "_master_current", "_master_prospects"):
        print "\t exporting " + table_name + " to .xlsx"
        qry = "SELECT * FROM %s;" % table_name

        res = db.query(qry)

        file_name = "/Users/connordog/Dropbox/Desktop_Files/Baseball/NSBL/%s_%s.xlsx" % (table_name, year)

        workbook = Workbook(file_name)

        sheet = workbook.add_worksheet()

        col_names_qry = """SELECT `COLUMN_NAME` 
        FROM `INFORMATION_SCHEMA`.`COLUMNS` 
        WHERE `TABLE_SCHEMA`='mlb_prospects' 
        AND `TABLE_NAME`='%s';"""
        col_names_query = col_names_qry % (table_name)

        col_names = db.query(col_names_query)

        for col_num, col_name in enumerate(col_names):
            cell_format = workbook.add_format()
            cell_format.set_bold()
            sheet.write(0, col_num, col_name[0], cell_format)

        for i, row in enumerate(res):
            cell_format = workbook.add_format()
            cell_format.set_shrink()
            for j, col in enumerate(row):
                if type(col) in (str,):
                    col = "".join([l if ord(l) < 128 else "" for l in col])
                sheet.write(i+1, j, col, cell_format)

        if table_name == "_draft_list":
            sheet.freeze_panes(1,8)
            sheet.autofilter('A1:DU1')

        elif table_name == "_master_current":
            sheet.freeze_panes(1,7)
            sheet.autofilter('A1:DT1')

        elif table_name == "_master_prospects":
            sheet.freeze_panes(1,10)
            sheet.autofilter('A1:DS1')


        workbook.set_size(1800,1200)
        workbook.close()


def export_masterCSV(table_name):
    print "\t exporting " + table_name + " to .csv"

    col_names_qry = """SELECT `COLUMN_NAME` 
    FROM `INFORMATION_SCHEMA`.`COLUMNS` 
    WHERE `TABLE_SCHEMA`='mlb_prospects' 
    AND `TABLE_NAME`='%s';"""
    col_names_query = col_names_qry % (table_name)

    col_names = db.query(col_names_query)

    columns = []
    for col_name in col_names:
        columns.append(col_name[0])

    csv_title = "/Users/connordog/Dropbox/Desktop_Files/Baseball/NSBL/%s.csv" % (table_name)
    csv_file = open(csv_title, "wb")
    append_csv = csv.writer(csv_file)
    append_csv.writerow(columns)

    qry = "SELECT * FROM %s;" % table_name

    res = db.query(qry)

    for row in res:
        row = list(row)
        for i, val in enumerate(row):
            if type(val) in (str,):
                row[i] = "".join([l if ord(l) < 128 else "" for l in val])
        append_csv.writerow(row)


if __name__ == "__main__":     
    parser = argparse.ArgumentParser()

    args = parser.parse_args()
    
    initiate()

