import argparse
from time import time
import csv
from xlsxwriter.workbook import Workbook
import os

from py_db import db
db = db("mlb_prospects")

year = 2022

def initiate():
    start_time = time()

    print "\n\ndeleting _master_prospects"
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
    export_masterCSV("_master_current")


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
    SELECT DISTINCT
    FORMAT(
    ( 5*avg_FV +
    0.50*IFNULL(COALESCE(FG_Pitchers_pOFP, FG_Hitters_pOFP), 0) + 
    1.25*IFNULL(COALESCE(FG_Pitchers_fOFP, FG_Hitters_fOFP), 0) + 
    0.75*IFNULL(COALESCE(MLB_Pitchers_OFP, MLB_Hitters_OFP), 0) 
    ) /
    (5 + 
    0.50*IFNULL((COALESCE(FG_Pitchers_pOFP, FG_Hitters_pOFP)/COALESCE(FG_Pitchers_pOFP, FG_Hitters_pOFP)), 0) + 
    1.25*IFNULL((COALESCE(FG_Pitchers_fOFP, FG_Hitters_fOFP)/COALESCE(FG_Pitchers_fOFP, FG_Hitters_fOFP)), 0) + 
    0.75*IFNULL((COALESCE(MLB_Pitchers_OFP, MLB_Hitters_OFP)/COALESCE(MLB_Pitchers_OFP, MLB_Hitters_OFP)), 0) 
    )
    + (IFNULL(MaxVelo_Bonus, 0) + IFNULL(FastballRPM_Bonus, 0) + IFNULL(BreakingRPM_Bonus, 0) + IFNULL(MaxEV_Bonus, 0) + IFNULL(HardHit_Bonus, 0) + IFNULL(Athleticism_Bonus, 0) + IFNULL(Performance_Bonus, 0) + IFNULL(Trend_Bonus, 0))
    , 1) AS superAdj_FV
    , FORMAT(
    ( 5*avg_FV +
    0.50*IFNULL(COALESCE(FG_Pitchers_pOFP, FG_Hitters_pOFP), 0) + 
    1.50*IFNULL(COALESCE(FG_Pitchers_fOFP, FG_Hitters_fOFP), 0) + 
    0.75*IFNULL(COALESCE(MLB_Pitchers_OFP, MLB_Hitters_OFP), 0) 
    ) /
    (5 + 
    0.50*IFNULL((COALESCE(FG_Pitchers_pOFP, FG_Hitters_pOFP)/COALESCE(FG_Pitchers_pOFP, FG_Hitters_pOFP)), 0) + 
    1.50*IFNULL((COALESCE(FG_Pitchers_fOFP, FG_Hitters_fOFP)/COALESCE(FG_Pitchers_fOFP, FG_Hitters_fOFP)), 0) + 
    0.75*IFNULL((COALESCE(MLB_Pitchers_OFP, MLB_Hitters_OFP)/COALESCE(MLB_Pitchers_OFP, MLB_Hitters_OFP)), 0) 
    )
    , 1) AS adj_FV
    , ofps.*
    FROM(
        SELECT
        FORMAT( 
        ( 5*IFNULL(fg_FV,0) + 3*IFNULL(mi_FV-3,0) + 2*IFNULL(MLB_FV-5,0) )
        /
        ( 5*IFNULL(fg_FV/fg_FV,0) + 3*IFNULL(mi_FV/mi_FV,0) + 2*IFNULL(MLB_FV/MLB_FV,0) ) 
        , 1) AS "avg_FV"
        , FORMAT(
        (
        0.25*IFNULL(COALESCE(FG_Pitchers_pOFP, FG_Hitters_pOFP), 0) + 
        2.75*IFNULL(COALESCE(FG_Pitchers_fOFP, FG_Hitters_fOFP), 0) + 
        1.00*IFNULL(COALESCE(MLB_Pitchers_OFP, MLB_Hitters_OFP), 0) 
        ) /
        (
        0.25*IFNULL((COALESCE(FG_Pitchers_pOFP, FG_Hitters_pOFP)/COALESCE(FG_Pitchers_pOFP, FG_Hitters_pOFP)), 0) + 
        2.75*IFNULL((COALESCE(FG_Pitchers_fOFP, FG_Hitters_fOFP)/COALESCE(FG_Pitchers_fOFP, FG_Hitters_fOFP)), 0) + 
        1.00*IFNULL((COALESCE(MLB_Pitchers_OFP, MLB_Hitters_OFP)/COALESCE(MLB_Pitchers_OFP, MLB_Hitters_OFP)), 0) 
        )
        , 1) AS ofp_FV
        , FORMAT(
        (
        3.00*IFNULL(COALESCE(FG_Pitchers_pOFP, FG_Hitters_pOFP), 0) + 
        1.00*IFNULL(COALESCE(MLB_Pitchers_OFP, MLB_Hitters_OFP), 0) 
        ) /
        (
        3.00*IFNULL((COALESCE(FG_Pitchers_pOFP, FG_Hitters_pOFP)/COALESCE(FG_Pitchers_pOFP, FG_Hitters_pOFP)), 0) + 
        1.00*IFNULL((COALESCE(MLB_Pitchers_OFP, MLB_Hitters_OFP)/COALESCE(MLB_Pitchers_OFP, MLB_Hitters_OFP)), 0) 
        )
        , 1) AS Scout_PV
        , FORMAT(
        (
        3.00*IFNULL(COALESCE(FG_Pitchers_fOFP, FG_Hitters_fOFP), 0) + 
        1.00*IFNULL(COALESCE(MLB_Pitchers_OFP, MLB_Hitters_OFP), 0) 
        ) /
        (
        3.00*IFNULL((COALESCE(FG_Pitchers_fOFP, FG_Hitters_fOFP)/COALESCE(FG_Pitchers_fOFP, FG_Hitters_fOFP)), 0) + 
        1.00*IFNULL((COALESCE(MLB_Pitchers_OFP, MLB_Hitters_OFP)/COALESCE(MLB_Pitchers_OFP, MLB_Hitters_OFP)), 0) 
        )
        , 1) AS Scout_FV
        , summary_stats.*
        FROM(
            SELECT "|" AS "*BIO*"
            , IF(IFNULL(mlb_fname,0)=IFNULL(fg_fname,0), mlb_fname, IFNULL(CONCAT(mlb_fname, ',', fg_fname), IFNULL(mlb_fname, fg_fname))) AS fnames
            , IF(IFNULL(mlb_lname,0)=IFNULL(fg_lname,0), mlb_lname, IFNULL(CONCAT(mlb_lname, ',', fg_lname), IFNULL(mlb_lname, fg_lname))) AS lnames
            , p.year
            , FORMAT(DATEDIFF(CONCAT(p.year, "-06-01"), CONCAT(p.birth_year,"-",p.birth_month,"-",p.birth_day)) / 365.25, 1) AS age
            , COALESCE(fg.position, fgd.position, mlbp.position, mlbd.position, mi.position) AS position
            , COALESCE(mlbp.bats, fg.bats, mlbd.bats, fgd.bats, "unknown") AS bats
            , COALESCE(mlbp.throws, fg.throws, mlbd.throws, fgd.throws, "unknown") AS throws
            , COALESCE(mlbp.height, fg.height, mlbd.height, fgd.height, "unknown") AS height
            , COALESCE(mlbp.weight, fg.weight, mlbd.weight, fgd.weight, "unknown") AS weight
            , IF(fgd.draft_rank IS NULL AND mlbd.rank IS NULL, "professional", "draft") AS p_type
            , ( 4*IFNULL(fg.FV,0) + 3*IFNULL(mi.FV,0) + 2*IFNULL((mlbp.FV-5),0) + 3*IFNULL(fgd.FV,0) + 1*IFNULL((mlbd.FV-5),0) ) AS "FV_pts"
            , ROUND(( 4*IFNULL(fg.FV/fg.FV,0) + 3*IFNULL(mi.FV/mi.FV,0) + 2*IFNULL(mlbp.FV/mlbp.FV,0) + 3*IFNULL(fgd.FV/fgd.FV,0) + 1*IFNULL(mlbd.FV/mlbd.FV,0) ), 0 ) AS "FV_weight"
            , "|" AS "*IDs*"
            , p.prospect_id
            , p.mlb_id
            , p.mlb_draft_id
            , p.fg_major_id
            , p.fg_minor_id
            , "|" AS "*FG*"
            , COALESCE(fg.ovr_rank, fgd.ovr_rank) AS FGOvrRnk
            , fgd.draft_rank AS FG_DraftRank
            , fg.org_rank AS FG_OrgRank
            , fgd.pick_num AS FG_DraftPick
            , COALESCE(fg.school, fgd.school) AS FGSchool
            , fg.level AS FG_Level
            , fg.signed AS FG_Signed
            , COALESCE(fg.team, fgd.pick_team) AS FG_Team
            , COALESCE(fg.levers, fgd.levers) AS FG_Levers
            , COALESCE(fg.athleticism, fgd.athleticism) AS FG_Athleticism
            , COALESCE(fg.performer, fgd.performer) AS FG_Performer
            , COALESCE(fg.risk, fgd.risk) AS FG_Risk
            , COALESCE(fg.variance, fgd.variance) AS FG_Variance
            , COALESCE(fg.eta, fgd.eta) AS FG_ETA
            , COALESCE(fg.pv, fgd.pv) AS FG_PV
            , COALESCE(fg.fv, fgd.fv) AS FG_FV
            , COALESCE(fg.video, fgd.video) AS FG_Video
            , COALESCE(fg.short_blurb, fgd.short_blurb) AS FG_ShortBlurb
            , COALESCE(fg.blurb, fgd.blurb) AS FG_Blurb
            , "|" AS "*mlb*"
            , COALESCE(mlbp.school_city, mlbd.school_city) AS MLB_School
            , COALESCE(mlbp.team, mlbd.team) AS MLB_Team
            , COALESCE(mlbp.drafted, mlbd.drafted) AS MLB_Drafted
            , COALESCE(mlbp.signed, mlbd.signed) AS MLB_Signed
            , COALESCE(mlbp.eta, mlbd.eta) AS MLB_ETA
            , COALESCE(mlbp.FV, mlbd.FV) AS MLB_FV
            , COALESCE(mlbp.blurb, mlbd.blurb) AS MLB_Blurb
            , "|" AS "*mi*"
            , mi.team AS mi_team
            , mi.team_rank AS mi_teamRank
            , mi.grade AS mi_grade
            , mi.eta as mi_eta
            , mi.FV AS mi_FV
            , "|" AS "*MLB_PRO*"
            , mlbp.rank AS MLB_OrgRank
            , mlbp.pre_top100 AS MLB_OvrRank
            , "|" AS "*MLB_DRAFT*"
            , mlbd.grade_country AS MLB_Grade
            , mlbd.college_commit AS MLB_Commit
            , "|" AS "*OFP*"
            , FORMAT( (4*fgh.Hit_present + 2*fgh.GamePower_present + 2*fgh.RawPower_present + 2*fgh.Field_present + 1*fgh.Speed_present)/11.00, 1) AS FG_Hitters_pOFP
            , FORMAT( (4*fgh.Hit_future + 2*fgh.GamePower_future + 2*fgh.RawPower_future + 2*fgh.Field_future + 1*fgh.Speed_future)/11.00, 1) AS FG_Hitters_fOFP
            , FORMAT( -2.5 + (4*mgh.hit + 4*mgh.power + 2*mgh.field + 1*mgh.run)/11.00, 1) AS MLB_Hitters_OFP
            , FORMAT( 
                (1+(3.5-(ISNULL(fgp.Fastball_present) + ISNULL(fgp.Changeup_present) + ISNULL(fgp.Curveball_present) + ISNULL(fgp.Slider_present) + ISNULL(fgp.Cutter_present) + ISNULL(fgp.Splitter_present)))/15) *
                (
                    (IFNULL(fgp.Fastball_present, 0) + IFNULL(fgp.Changeup_present, 0) + 
                    IFNULL(fgp.Curveball_present, 0) + IFNULL(fgp.Slider_present, 0) +
                    IFNULL(fgp.Cutter_present, 0) + IFNULL(fgp.Splitter_present, 0) +
                    1.5*IFNULL(fgp.Command_present, 0)
                    )/
                    (IFNULL(fgp.Fastball_present/fgp.Fastball_present, 0) + IFNULL(fgp.Changeup_present/fgp.Changeup_present, 0) + 
                    IFNULL(fgp.Curveball_present/fgp.Curveball_present, 0) + IFNULL(fgp.Slider_present/fgp.Slider_present, 0) +
                    IFNULL(fgp.Cutter_present/fgp.Cutter_present, 0) + IFNULL(fgp.Splitter_present/fgp.Splitter_present, 0) +
                    1.5*IFNULL(fgp.Command_present/fgp.Command_present, 0)
                    )
                )
            , 1) AS FG_Pitchers_pOFP
            , FORMAT( 
                (1+(3.5-(ISNULL(fgp.Fastball_future) + ISNULL(fgp.Changeup_future) + ISNULL(fgp.Curveball_future) + ISNULL(fgp.Slider_future) + ISNULL(fgp.Cutter_future) + ISNULL(fgp.Splitter_future)))/15) *
                (
                    (IFNULL(fgp.Fastball_future, 0) + IFNULL(fgp.Changeup_future, 0) + 
                    IFNULL(fgp.Curveball_future, 0) + IFNULL(fgp.Slider_future, 0) +
                    IFNULL(fgp.Cutter_future, 0) + IFNULL(fgp.Splitter_future, 0) +
                    1.5*IFNULL(fgp.Command_future, 0)
                    )/
                    (IFNULL(fgp.Fastball_future/fgp.Fastball_future, 0) + IFNULL(fgp.Changeup_future/fgp.Changeup_future, 0) + 
                    IFNULL(fgp.Curveball_future/fgp.Curveball_future, 0) + IFNULL(fgp.Slider_future/fgp.Slider_future, 0) +
                    IFNULL(fgp.Cutter_future/fgp.Cutter_future, 0) + IFNULL(fgp.Splitter_future/fgp.Splitter_future, 0) +
                    1.5*IFNULL(fgp.Command_future/fgp.Command_future, 0)
                    )
                )
            , 1) AS FG_Pitchers_fOFP,
            FORMAT(
                (1+(3.5-(ISNULL(mgp.fastball) + ISNULL(mgp.change) + ISNULL(mgp.curve) + ISNULL(mgp.slider) + ISNULL(mgp.cutter) + ISNULL(mgp.splitter) + ISNULL(mgp.other)))/15) *
                (
                    -5.0 +
                    (IFNULL(mgp.fastball, 0) + IFNULL(mgp.change, 0) + 
                    IFNULL(mgp.curve, 0) + IFNULL(mgp.slider, 0) +
                    IFNULL(mgp.cutter, 0) + IFNULL(mgp.splitter, 0) +
                    IFNULL(mgp.other, 0) + 1.5*IFNULL(mgp.control, 0)
                    )/
                    (IFNULL(mgp.fastball/mgp.fastball, 0) + IFNULL(mgp.change/mgp.change, 0) + 
                    IFNULL(mgp.curve/mgp.curve, 0) + IFNULL(mgp.slider/mgp.slider, 0) +
                    IFNULL(mgp.cutter/mgp.cutter, 0) + IFNULL(mgp.splitter/mgp.splitter, 0) +
                    IFNULL(mgp.other/mgp.other, 0) + 1.5*IFNULL(mgp.control/mgp.control, 0)
                    )
                )
            , 1) AS MLB_Pitchers_OFP
            , "|" AS "*BONUS_OFP*"
            , LEAST(GREATEST((MaxVelo-94)/4, 0), 2) AS MaxVelo_Bonus
            , LEAST(GREATEST((Fastball_RPM-2500)/300, 0), 2) AS FastballRPM_Bonus
            , LEAST(GREATEST((Breaking_RPM-2700)/300, 0), 2) AS BreakingRPM_Bonus
            , LEAST(GREATEST((fgh.Max_EV-107)/4, -2), 2) AS MaxEV_Bonus
            , LEAST(GREATEST((fgh.HardHit_Pct-0.3)/0.1, -2), 2) AS HardHit_Bonus
            , 1.0*(COALESCE(fg.athleticism, fgd.athleticism)) AS Athleticism_Bonus
            , 1.0*COALESCE(fg.performer, fgd.performer) AS Performance_Bonus
            , IF(COALESCE(fg.trend, fgd.trend) = 'UP', 1.0, IF(COALESCE(fg.trend, fgd.trend) = 'DOWN', -1.0, 0)) AS Trend_Bonus
            , "|" AS "*FG_HIT*"
            , fgh.Hit_present, fgh.GamePower_present, fgh.RawPower_present, fgh.Speed_present, fgh.Field_present, fgh.Throws_present
            , fgh.Hit_future, fgh.GamePower_future, fgh.RawPower_future, fgh.Speed_future, fgh.Field_future, fgh.Throws_future
            , fgh.Max_EV, fgh.HardHit_Pct
            , "|" AS "*FG_PITCH*"
            , fgp.TJ_Date
            , fgp.Fastball_RPM
            , fgp.Breaking_RPM
            , fgp.Command_present, fgp.Fastball_present, fgp.Changeup_present, fgp.Curveball_present, fgp.Slider_present, fgp.Cutter_present, fgp.Splitter_present
            , fgp.Command_future, fgp.Fastball_future, fgp.Changeup_future, fgp.Curveball_future, fgp.Slider_future, fgp.Cutter_future, fgp.Splitter_future
            , "|" AS "*MLB_HIT*"
            , mgh.hit, mgh.power, mgh.run, mgh.arm, mgh.field
            , "|" AS "*MLB_PITCH*"
            , mgp.fastball, mgp.change, mgp.curve, mgp.slider, mgp.cutter, mgp.splitter, mgp.other, mgp.control
            FROM (SELECT *, %s AS year FROM professional_prospects) p
            LEFT JOIN fg_prospects_professional fg USING (YEAR, prospect_id)
            LEFT JOIN minorleagueball_professional mi USING (YEAR, prospect_id)
            LEFT JOIN mlb_prospects_professional mlbp USING (YEAR, prospect_id)
            LEFT JOIN fg_prospects_draft fgd USING (YEAR, prospect_id)
            LEFT JOIN mlb_prospects_draft mlbd USING (YEAR, prospect_id)
            LEFT JOIN fg_grades_hitters fgh ON (p.year = fgh.year AND COALESCE(fg.grades_id, fgd.grades_id) = fgh.grades_id)
            LEFT JOIN fg_grades_pitchers fgp ON (p.year = fgp.year AND COALESCE(fg.grades_id, fgd.grades_id) = fgp.grades_id)
            LEFT JOIN mlb_grades_hitters mgh ON (p.year = mgh.year AND (mlbp.grades_id = mgh.grades_id OR mlbd.grades_id = mgh.grades_id))
            LEFT JOIN mlb_grades_pitchers mgp ON (p.year = mgp.year AND (mlbp.grades_id = mgp.grades_id OR mlbd.grades_id = mgp.grades_id)) 
            WHERE 1
                AND (0
                    OR fg.year IS NOT NULL 
                    OR mi.year IS NOT NULL
                    OR mlbp.year IS NOT NULL
                    OR fgd.year IS NOT NULL
                    OR mlbd.year IS NOT NULL
                )

        ) summary_stats
    ) ofps
    GROUP BY superAdj_FV DESC, adj_FV, avg_FV, ofp_FV, fnames, lnames, year, age, position, bats, throws, height, weight
    """

    table_query = table_qry % (table_add, year)
    # raw_input(table_query)
    return table_query


def update_tables(year):
    qry = """SET @draft_rnk = 0;
    SET @rowno1 = 0; 
    SET @rowno2 = 0; 
    SET @rowno3 = 0; 
    SET @rowno4 = 0;

    DROP TABLE IF EXISTS _master_current;
    CREATE TABLE _master_current AS
    SELECT DISTINCT a.*
    FROM(
        SELECT superAdjFV_rnk
        , adjFV_rnk
        , avgFV_rnk
        , ofpFV_rnk
        , m.*
        , GROUP_CONCAT(DISTINCT cr.team_abb ORDER BY cr.salary DESC) AS NSBL_Team
        , GROUP_CONCAT(DISTINCT cr.salary ORDER BY cr.salary DESC) AS NSBL_Salary
        , GROUP_CONCAT(DISTINCT cr.contract_year ORDER BY cr.salary DESC) AS NSBL_Year
        , GROUP_CONCAT(DISTINCT CONCAT(cr.salary, '/', cr.contract_year, ' - ', cr.team_abb) ORDER BY cr.salary DESC SEPARATOR ' | ') AS NSBL_contract
        FROM(
            SELECT @rowno1:=@rowno1+1 AS `superAdjFV_rnk`, fnames, lnames, age
            FROM(
                SELECT m.*
                FROM _master_prospects m
                WHERE 1
                    AND m.year = %s
                ORDER BY superAdj_FV DESC
            ) a1
        ) a2
        JOIN(
            SELECT @rowno2:=@rowno2+1 AS `adjFV_rnk`, fnames, lnames, age
            FROM(
                SELECT m.*
                FROM _master_prospects m
                WHERE 1
                    AND m.year = %s
                ORDER BY adj_FV DESC
            ) b1
        ) b2 USING (fnames, lnames, age)
        JOIN(
            SELECT @rowno3:=@rowno3+1 AS `avgFV_rnk`, fnames, lnames, age
            FROM(
                SELECT m.*
                FROM _master_prospects m
                WHERE 1
                    AND m.year = %s
                ORDER BY avg_FV DESC
            ) c1
        ) c2 USING (fnames, lnames, age)
        JOIN(
            SELECT @rowno4:=@rowno4+1 AS `ofpFV_rnk`, fnames, lnames, age
            FROM(
                SELECT m.*
                FROM _master_prospects m
                WHERE 1
                    AND m.year = %s
                ORDER BY ofp_FV DESC
            ) d1
        ) d2 USING (fnames, lnames, age)
        JOIN _master_prospects m USING (fnames, lnames, age)
        JOIN professional_prospects pp ON (m.prospect_id = pp.prospect_id)
        LEFT JOIN NSBL.name_mapper nm ON (1
            AND (0
                OR CONCAT(pp.mlb_fname, ' ', pp.mlb_lname) = nm.wrong_name
                OR CONCAT(pp.mlb_fname, ' ', pp.fg_lname) = nm.wrong_name
                OR CONCAT(pp.fg_fname, ' ', pp.mlb_lname) = nm.wrong_name
                OR CONCAT(pp.fg_fname, ' ', pp.fg_lname) = nm.wrong_name
            )
            AND (nm.start_year IS NULL OR nm.start_year <= m.year)
            AND (nm.end_year IS NULL OR nm.end_year >= m.year)
            AND (nm.position = '' OR nm.position = m.position)
            AND (nm.rl_team = '' OR nm.rl_team = m.FG_Team)
            # AND (nm.nsbl_team = '' OR nm.nsbl_team = rbp.team_abb)
        )
        LEFT JOIN NSBL.name_mapper nm2 ON (nm.right_fname = nm2.right_fname
            AND nm.right_lname = nm2.right_lname
            AND (nm.start_year IS NULL OR nm.start_year = nm2.start_year)
            AND (nm.end_year IS NULL OR nm.end_year = nm2.end_year)
            AND (nm.position = '' OR nm.position = nm2.position)
            AND (nm.rl_team = '' OR nm.rl_team = nm2.rl_team)
        )
        LEFT JOIN NSBL._draft_rosters cr ON (
            nm2.wrong_name = CONCAT(cr.fname, ' ', cr.lname)
            OR
            (
                find_in_set(
                    REPLACE(REPLACE(REPLACE(REPLACE(cr.fname,".","")," JR",""),"-"," "),"'","")
                    , REPLACE(REPLACE(REPLACE(REPLACE(m.fnames,".","")," JR",""),"-"," "),"'","")
                )>=1
                AND find_in_set(
                    REPLACE(REPLACE(REPLACE(REPLACE(cr.lname,".","")," JR",""),"-"," "),"'","")
                    , REPLACE(REPLACE(REPLACE(REPLACE(m.lnames,".","")," JR",""),"-"," "),"'","")
                )>=1
            )
        )
        WHERE 1
            AND m.year = %s
        GROUP BY nm.right_fname, nm.right_lname
    ) a
    ORDER BY superAdjFV_rnk ASC
    ;


    DROP TABLE IF EXISTS _draft_list;
    CREATE TABLE _draft_list AS
    SELECT CONCAT(IF(LOCATE(",", fnames) > 0, LEFT(fnames, POSITION("," in fnames)-1), fnames), " ", IF(LOCATE(",", lnames) > 0, LEFT(lnames, POSITION("," in lnames)-1), lnames)) AS full_name
    , "" AS drafted
    , age AS dAge
    , position AS dPos
    , COALESCE(FG_Team, MLB_Team) AS dTeam
    , COALESCE(FG_Signed, MLB_Drafted, MLB_Signed) AS dSigned
    , @draft_rnk := @draft_rnk+1 AS DraftRank
    , a.*
    FROM(
        SELECT *
        FROM _master_current m
        WHERE 1
            AND m.NSBL_Team IS NULL
        ORDER BY superAdjFV_rnk ASC
    ) a
    HAVING 1
        AND full_name NOT IN ('Julio Rodriguez', 'Carlos Colmenarez', 'Wilman Diaz', 'Cristian Hernandez', 'Jackson Chourio', 'Cristian Santana', 'Andry Lara', 'Pedro Pineda', 'Pedro Leon')
    ;
    """

    query_full = qry % (year, year, year, year, year)

    for query in query_full.split(";")[:-1]:
        db.query(query)
        db.conn.commit()


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
            sheet.autofilter('A1:EN1')

        elif table_name == "_master_current":
            sheet.freeze_panes(1,16)
            sheet.autofilter('A1:EG1')

        elif table_name == "_master_prospects":
            sheet.freeze_panes(1,12)
            sheet.autofilter('A1:DY1')


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

    csv_title = "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/MLB_Prospects_%s.csv" % (table_name.replace("_",""))
    csv_file = open(csv_title, "wb")
    append_csv = csv.writer(csv_file)
    append_csv.writerow(columns)

    qry = "SELECT * FROM %s;" % table_name

    res = db.query(qry)

    for row in res:
        row = list(row)
        for i, val in enumerate(row):
            if type(val) in (str,):
                row[i] = '"' + "".join([l if ord(l) < 128 else "" for l in val]).replace("<o>","").replace("<P>","") + '"'
        append_csv.writerow(row)


if __name__ == "__main__":     
    parser = argparse.ArgumentParser()

    args = parser.parse_args()
    
    initiate()

