# A set of helper functions for the mlb_prospects codebase
from datetime import date, datetime, timedelta


from py_db import db
db = db("mlb_prospects")


def fname_lookup(fname):
    if fname in ("Mike", "Michael", "Mikey"):
        fname_search = "Mi"
    elif fname in ("Nick", "Nicholas"):
        fname_search = "Nic"
    elif fname in ("Jake", "Jacob", "Jakob"):
        fname_search = "Ja"
    elif fname in ("Tom", "Thomas","Tommy","Thommy"):
        fname_search = "om"
    elif fname in ("Luke", "Lucas", "Lukas"):
        fname_search = "Lu"
    elif fname in ("Jay", "Jason", "Jayson"):
        fname_search = "Ja"
    elif fname in ("Manny", "Manuel", "Emmanuel"):
        fname_search = "Man"
    elif fname in ("Ozzie", "Ozhaino"):
        fname_search = "Oz"
    elif fname in ("Antonio", "Tony"):
        fname_search = "Ton"
    elif fname in ("Jon", "John", "Jonny", "Johnny", "Jonathan"):
        fname_search = "Jo"
    elif fname in ( "Joe", "Joseph", "Joey"):
        fname_search = "Jo"
    elif fname in ("Jazz", "Jasrado"):
        fname_search = "Ja"
    elif fname in ("Stephen", "Steve", "Steven"):
        fname_search = "Ste"
    elif fname in ("Nathan", "Nathaniel", "Nate"):
        fname_search = "Nat"
    elif fname in ("Ron", "Ronald", "Ronny", "Ronnie", "Ronaldo"):
        fname_search = "Ron"
    else:
        fname_search = fname

    return fname_search


def id_lookup(fname, lname, lower_year, upper_year):
    """
    Tries to find the prospect_id given a prospects first name (fname), last name (lname), and a range of years they could have been born in (lower_year, upper_year)
    """
    fname_search = fname_lookup(fname)

    search_qry = """SELECT prospect_id, birth_year, birth_month, birth_day, COUNT(*)
    FROM professional_prospects 
    WHERE birth_year >= %s 
    AND birth_year <= %s
    AND (
        ( REPLACE(REPLACE(REPLACE(REPLACE(mlb_lname, ".", ""),"'",""),"-","")," ","") 
        LIKE REPLACE(REPLACE(REPLACE(REPLACE("%%%s%%", ".", ""),"'",""),"-","")," ","") ) OR 
        ( REPLACE(REPLACE(REPLACE(REPLACE("%s",".",""),"'",""),"-","")," ","")
        LIKE REPLACE(REPLACE(REPLACE(REPLACE(CONCAT("%%",mlb_lname,"%%"), ".", ""),"'",""),"-","")," ","") ) OR 
        ( REPLACE(REPLACE(REPLACE(REPLACE(fg_lname, ".", ""),"'",""),"-","")," ","")
        LIKE REPLACE(REPLACE(REPLACE(REPLACE("%%%s%%", ".", ""),"'",""),"-","")," ","") ) OR 
        ( REPLACE(REPLACE(REPLACE(REPLACE("%s", ".", ""),"'",""),"-","")," ","")
        LIKE REPLACE(REPLACE(REPLACE(REPLACE(CONCAT("%%",fg_lname,"%%"), ".", ""),"'",""),"-","")," ","") )
        )
    AND (
        ( REPLACE(REPLACE(REPLACE(REPLACE(mlb_fname, ".", ""),"'",""),"-","")," ","")
        LIKE REPLACE(REPLACE(REPLACE(REPLACE("%%%s%%", ".", ""),"'",""),"-","")," ","") ) OR 
        ( REPLACE(REPLACE(REPLACE(REPLACE("%s",".",""),"'",""),"-","")," ","") 
        LIKE REPLACE(REPLACE(REPLACE(REPLACE(CONCAT("%%",mlb_fname,"%%"), ".", ""),"'",""),"-","")," ","") ) OR 
        ( REPLACE(REPLACE(REPLACE(REPLACE(fg_fname, ".", ""),"'",""),"-","")," ","")
        LIKE REPLACE(REPLACE(REPLACE(REPLACE("%%%s%%", ".", ""),"'",""),"-","")," ","") ) OR 
        ( REPLACE(REPLACE(REPLACE(REPLACE("%s", ".", ""),"'",""),"-","")," ","")
        LIKE REPLACE(REPLACE(REPLACE(REPLACE(CONCAT("%%",fg_fname,"%%"), ".", ""),"'",""),"-","")," ","") )
        )
    ;"""

    search_query = search_qry % (lower_year, upper_year, lname, lname, lname, lname, fname_search, fname_search, fname_search, fname_search)
    # raw_input(search_query)
    player_id, byear, bmonth, bday, player_cnt = db.query(search_query)[0]

    if player_cnt == 1:
        prospect_id = player_id
    else:
        prospect_id = 0
        byear, bmonth, bday = None, None, None

    return prospect_id, byear, bmonth, bday


def add_prospect(site_id, fname, lname, byear, bmonth, bday, p_type, id_type='all'):
    """
    Looks up a prospets prospect_id given their first name (fname) last name (lname), site id (site_id), site (p_type), and birthdate (byear, bmonth, bday).
    If no prospect is found, adds the player to the professional_prospects table and returns the newly created prospect_id.
    """

    fname_search = fname_lookup(fname)

    if id_type == 'all':
        qry_add = """((mlb_id = "%s" AND mlb_id != 0)
        OR (mlb_draft_id = "%s" AND mlb_draft_id IS NOT NULL)
        OR (mlb_international_id = "%s" AND mlb_international_id IS NOT NULL)
        OR (fg_minor_id = "%s" AND fg_minor_id IS NOT NULL)
        OR (fg_major_id = "%s" AND fg_major_id IS NOT NULL))""" % (site_id, site_id, site_id, site_id, site_id)
    else:
        qry_add = """(%s = "%s" AND (%s != 0 OR %s IS NOT NULL))""" % (id_type, site_id, id_type, id_type)
        
    check_qry = """SELECT prospect_id
    FROM professional_prospects
    WHERE 1
        AND %s
    ;
    """

    check_query = check_qry % (qry_add)
    check_val = db.query(check_query)

    if check_val != ():
        prospect_id = check_val[0][0]
        return prospect_id
    else:
        check_other_qry = """SELECT prospect_id
        FROM professional_prospects 
        WHERE birth_year = %s
        AND birth_month = %s
        AND birth_day = %s
        AND (
            ( REPLACE(REPLACE(REPLACE(REPLACE(mlb_lname, ".", ""),"'",""),"-","")," ","") 
            LIKE REPLACE(REPLACE(REPLACE(REPLACE("%%%s%%", ".", ""),"'",""),"-","")," ","") ) OR 
            ( REPLACE(REPLACE(REPLACE(REPLACE("%s",".",""),"'",""),"-","")," ","")
            LIKE REPLACE(REPLACE(REPLACE(REPLACE(CONCAT("%%",mlb_lname,"%%"), ".", ""),"'",""),"-","")," ","") ) OR 
            ( REPLACE(REPLACE(REPLACE(REPLACE(fg_lname, ".", ""),"'",""),"-","")," ","")
            LIKE REPLACE(REPLACE(REPLACE(REPLACE("%%%s%%", ".", ""),"'",""),"-","")," ","") ) OR 
            ( REPLACE(REPLACE(REPLACE(REPLACE("%s", ".", ""),"'",""),"-","")," ","")
            LIKE REPLACE(REPLACE(REPLACE(REPLACE(CONCAT("%%",fg_lname,"%%"), ".", ""),"'",""),"-","")," ","") )
            )
        AND (
            ( REPLACE(REPLACE(REPLACE(REPLACE(mlb_fname, ".", ""),"'",""),"-","")," ","")
            LIKE REPLACE(REPLACE(REPLACE(REPLACE("%%%s%%", ".", ""),"'",""),"-","")," ","") ) OR 
            ( REPLACE(REPLACE(REPLACE(REPLACE("%s",".",""),"'",""),"-","")," ","") 
            LIKE REPLACE(REPLACE(REPLACE(REPLACE(CONCAT("%%",mlb_fname,"%%"), ".", ""),"'",""),"-","")," ","") ) OR 
            ( REPLACE(REPLACE(REPLACE(REPLACE(fg_fname, ".", ""),"'",""),"-","")," ","")
            LIKE REPLACE(REPLACE(REPLACE(REPLACE("%%%s%%", ".", ""),"'",""),"-","")," ","") ) OR 
            ( REPLACE(REPLACE(REPLACE(REPLACE("%s", ".", ""),"'",""),"-","")," ","")
            LIKE REPLACE(REPLACE(REPLACE(REPLACE(CONCAT("%%",fg_fname,"%%"), ".", ""),"'",""),"-","")," ","") )
            )
        ;"""

        check_other_query = check_other_qry % (byear, bmonth, bday, lname, lname, lname, lname, fname_search, fname_search, fname_search, fname_search)
        check_other_val = db.query(check_other_query)

        if check_other_val != ():
            prospect_id = check_other_val[0][0]

            f_name = "mlb_fname"
            l_name = "mlb_lname"
            if p_type == "professional":
                id_column = "mlb_id"
            elif p_type == "draft":
                id_column = "mlb_draft_id"
            elif p_type == "int":
                id_column = "mlb_international_id"
            elif p_type == "fg":
                if site_id[0] == "s":
                    id_column = "fg_minor_id"
                else:
                    id_column = "fg_major_id"
                f_name = "fg_fname"
                l_name = "fg_lname"

            print "\n\n\t\t\tadding", fname, lname, id_column, site_id, '\n\n'

            for col, val in {f_name:fname, l_name:lname, id_column:site_id}.items():

                set_str = 'SET %s = "%s"' % (col,val)
                set_str2 = "AND (%s IS NULL OR %s IS NULL)" % (col, col)

                update_qry = """UPDATE professional_prospects 
                %s
                WHERE prospect_id = %s 
                %s;"""


                update_query = update_qry % (set_str, prospect_id, set_str2)
                db.query(update_query)
                db.conn.commit()

            return prospect_id

        else:
            entry = {"birth_year":int(byear), "birth_month":int(bmonth), "birth_day":int(bday)}

            if p_type == "fg":
                if site_id[0] == "s":
                    entry["fg_minor_id"] = site_id
                else:
                    entry["fg_major_id"] = site_id
                entry["fg_fname"] = fname
                entry["fg_lname"] = lname
            else:
                entry["mlb_fname"] = fname
                entry["mlb_lname"] = lname
                if p_type == "professional":
                    entry["mlb_id"] = site_id
                elif p_type == "draft":
                    entry["mlb_draft_id"] = site_id
                elif p_type == "int":
                    entry["mlb_international_id"] = site_id

            db.insertRowDict(entry, "professional_prospects", debug=1)
            db.conn.commit()

            print '\n\n\n\n', check_other_query, '\n\n\n\n\n', check_query, '\n\n\n\n'
            recheck_val = db.query(check_query)
            prospect_id = recheck_val[0][0]
            return prospect_id


def est_fg_birthday(age, year, list_type):
    """
    Estimates a player's birthday given their listed age (age), what year (year) and whether they are a draft or international prospect (list_type).
    """

    if list_type in ("draft", "professional"):
        reference_date = datetime(year=year, month=06, day=15)
    elif list_type == "international":
        reference_date = datetime(year=year, month=07, day=02)

    days = (float(age)*365.25)
    birthday_est = reference_date - timedelta(days=days)

    est_year = birthday_est.year
    if (birthday_est.month >= 5 or birthday_est.month <= 8):
        lower_year = est_year - 1
        upper_year = est_year + 1
    elif (birthday_est.month > 8):
        lower_year = est_year
        upper_year = est_year + 1
    else:
        lower_year = est_year - 1
        upper_year = est_year

    return lower_year, upper_year


def adjust_mlb_names(mlb_id, fname, lname):
    """
    Adjusts a prospect's first and last name (fname, lname) given their mlb.com player_id for better usage in matching to the professional_prospects table.
    """
    names_dict = {
    "clark_trenton": ["Trent", "Grisham"],
    "deleon_juan": ["Juan", "De Leon"],
    "deleon_michael": ["Michael", "De Leon"],
    "eshelman_thomas": ["Tom", "Eshelman"],
    "gatewood_jacob": ["Jake", "Gatewood"],
    "groome_jason": ["Jay", "Groome"],
    "hall_dl": ["DL", "Hall"],
    "harrison_kj": ["KJ", "Harrison"],
    "machado_jonathan": ["Jonatan", "Machado"],
    "martinez_eddie": ["Eddy", "Martinez"],
    "pablo_martinez_julio": ["Julio Pablo", "Martinez"],
    "samuel_franco_wander": ["Wander", "Franco"],
    "sanchez_hudson": ["Hudson", "Potts"],
    "santillan_antonio": ["Tony", "Santillan"],
    "stewart_dj": ["DJ", "Stewart"],
    "yamamoto_jordan": ["Jordan", "Yamamoto"],
    "zapata_micker_adolfo": ["Micker", "Adolfo"],
    593423: ["Frankie", "Montas"],
    595222: ["Mike", "Gerber"],
    596001: ["Jakob", "Junis"],
    607188: ["Jake", "Faria"],
    621072: ["Nick", "Travieso"],
    621466: ["DJ", "Stewart"],
    645277: ["Ozzie", "Albies"],
    650520: ["Micker", "Adolfo"],
    650958: ["Michael", "De Leon"],
    656449: ["Jake", "Gatewood"],
    657141: ["Jordan", "Yamamoto"],
    660665: ["Juan", "De Leon"],
    663574: ["Tony", "Santillan"],
    663757: ["Trent", "Grisham"],
    664045: ["Tom", "Eshelman"],
    668888: ["Hudson", "Potts"],
    671054: ["Jonatan", "Machado"],
    677551: ["Wander", "Franco"],
    679881: ["Julio Pablo", "Martinez"],

    }

    if mlb_id in names_dict:
        fname, lname = names_dict.get(mlb_id)
        return fname, lname
    else:
        return fname, lname


def adjust_mlb_positions(mlb_id, position):
    """
    Adjusts a prospect's position given their mlb.com player_id (mlb_id).
    Not heavily necessary unless a player has been mis-classified as a pitcher when they should be a hitter or vice versa.
    """
    position_dict = {
    "ryan_ryder": "RHP",
    "taylor_blake": "LHP",
    642130: "LHP",
    669160: "RHP",
    }

    if mlb_id in position_dict:
        position = position_dict.get(mlb_id)
        return position
    else:
        return position


def adjust_mlb_birthdays(mlb_id, byear, bmonth, bday):
    """
    Adjusts a prospect's birthday given their mlb.com birthdate (byear, bmonth, bday).
    Mostly used in adjusted wrong birthdates for draft prospects in earlier seasons.
    """
    birthday_dict = {
    "agnos_jake": [1998, 5, 23],
    "allen_logan": [1997, 5, 23],
    "aracena_ricky": [1997, 10, 2],
    "bradley_bobby": [1996, 5, 29],
    "burdi_zack": [1995, 3, 9],
    "burr_ryan": [1994, 5, 28],
    "cairo_christian": [2001, 6, 11],
    "castillo_diego": [1994, 1, 18],
    "cody_kyle": [1994, 8, 9],
    "deetz_dean": [1993, 11, 29],
    "diaz_lewin": [1996, 11, 19],
    "dietz_matthias": [1995, 9, 20],
    "dillard_thomas": [1997, 8, 28],
    "eastman_colton": [1996, 8, 22],
    "ervin_phillip": [1992, 7, 15],
    "farmer_buck": [1991, 2, 20],
    "fletcher_dominic": [1997, 9, 2],
    "garcia_victor": [1999, 9, 16],
    "gingery_steven": [1997, 9, 23],
    "gray_seth": [1998, 5, 30],
    "green_hunter": [1995, 7, 12],
    "hayes_kebryan": [1997, 1, 28],
    "hays_austin": [1995, 7, 5],
    "henry_tommy": [1997, 7, 29],
    "hill_brigham": [1995, 7, 8],
    "hudson_dakota": [1994, 9, 15],
    "jewell_jake": [1993, 5, 16],
    "justus_connor": [1994, 11, 2],
    "kirby_nathan": [1993, 11, 23],
    "knebel_corey": [1991, 11, 26],
    "lee_nick": [1991, 1, 13],
    "lopez_jose": [1993, 9, 1],
    "mathias_mark": [1994, 8, 2],
    "mitchell_calvin": [1999, 3, 8],
    "molina_leonardo": [1997, 7, 31],
    "morris_tanner": [1998, 9, 13],
    "murphy_brendan": [1999, 1, 2],
    "murphy_sean": [1994, 10, 10],
    "oliva_jared": [1995, 11, 27],
    "perez_joe": [1999, 8, 12],
    "quantrill_cal": [1995, 2, 10],
    "rainey_tanner": [1992, 12, 25],
    "riley_austin": [1997, 4, 2],
    "rodriguez_jose": [1995, 8, 29],
    "rosario_jeisson": [1999, 10, 22],
    "shipley_braden": [1992, 2, 22],
    "torres_gleyber": [1996, 12, 13],
    "triolo_jared": [1998, 2, 8],
    "tyler_robert": [1995, 6, 18],
    "uelmen_erich": [1996, 5, 19],
    "varsho_daulton": [1996, 7, 2],
    "wakamatsu_luke": [1996, 10, 10],
    "ward_taylor": [1993, 12, 14],
    "weathers_ryan": [1999, 12, 17],
    "weigel_patrick": [1994, 7, 8],
    "whitley_forrest": [1997, 9, 15],
    "wise_carl": [1994, 5, 25],
    "woodford_jake": [1996, 10, 28],
    "zagunis_mark": [1993, 2, 5],
    "little_grant": [1997, 7, 8],
    "jarvis_justin": [2000, 2, 20],
    }

    if mlb_id in birthday_dict:
        byear, bmonth, bday = birthday_dict.get(mlb_id)
        return byear, bmonth, bday
    else:
        return byear, bmonth, bday


def adjust_fg_names(full_name):
    """
    Splits a players full name into first and last names and returns those values.
    Also will adjust a player's name if their name has been listed non ideally so we can better match them to the professional_prospects table.
    """
    names_dict = {
    "Abraham Gutierrez": ["Abrahan", "Gutierrez"],
    "Adam Brett Walker": ["Adam Brett", "Walker"],
    "Adolis Garcia": ["Jose Adolis", "Garcia"],
    "D.J. Stewart": ["DJ", "Stewart"],
    "Fernando Tatis, Jr.": ["Fernando", "Tatis Jr."],
    "Hoy Jun Park": ["Hoy Jun", "Park"],
    "Jeison Rosario": ["Jeisson", "Rosario"],
    "Joe Gray, Jr.": ["Joe", "Gray Jr."],
    "Jonathan Machado": ["Jonatan", "Machado"],
    "Lenny Torres, Jr.": ["Lenny", "Torres Jr."],
    "Luis Alejandro Basabe": ["Luis Alejandro", "Basabe"],
    "Luis Alexander Basabe": ["Luis Alexander", "Basabe"],
    "M.J. Melendez": ["MJ", "Melendez"],
    "Mc Gregory Contreras": ["Mc Gregory", "Contreras"],
    "Michael Soroka": ["Mike", "Soroka"],
    "Nate Kirby": ["Nathan", "Kirby"],
    "Onil Cruz": ["Oneil", "Cruz"],
    "Roland Bolanos": ["Ronald", "Bolanos"],
    "T.J. Friedl": ["TJ", "Friedl"],
    "Thomas Eshelman": ["Tom", "Eshelman"],
    "TJ Zeuch": ["T.J.", "Zeuch"],
    "Trenton Clark": ["Trent", "Grisham"],
    "Vladimir Guerrero, Jr.": ["Vladimir", "Guerrero Jr."],
    "Yordy Barley": ["Jordy", "Barley"],
    }

    if full_name in names_dict:
        fname, lname = names_dict.get(full_name)
        full_name = fname + " " + lname
        return full_name, fname, lname
    else:
        fname, lname = [full_name.split(" ")[0], " ".join(full_name.split(" ")[1:])]
        return full_name, fname, lname


def adjust_fg_positions(fg_id, positions):
    """
    Adjusts a prospect's position given their fangraphs player_id (fg_id).
    Not heavily necessary unless a player has been mis-classified as a pitcher when they should be a hitter or vice versa.
    """
    positions_dict = {
    }

    if fg_id in positions_dict:
        positions = positions_dict.get(fg_id)
        return positions
    else:
        return positions


def adjust_fg_positions2(full_name, position):
    """
    Adjusts a prospect's position given their fangraphs player_id (fg_id).
    Not heavily necessary unless a player has been mis-classified as a pitcher when they should be a hitter or vice versa.
    """
    names_dict = {
    }
 
    if full_name in names_dict:
        position = names_dict.get(full_name)
        return position
    else:
        return position


def adjust_fg_birthdays(fg_id, byear, bmonth, bday): 
    """
    Adjusts a prospect's birthday given their fangraphs birthdate (byear, bmonth, bday) and fangraphs id (fg_id).
    """
    birthday_dict = {
    "14510": ["14510", 1993, 7, 1],
    "16207": ["16207", 1992, 9, 18],
    "16401": ["16401", 1993, 12, 26],
    "17548": ["17548", 1993, 12, 14],
    "18126": ["18126", 1994, 1, 1],
    "sa293098": ["sa874117", 1995, 10, 2],
    "sa3005715": ["sa3005715", 2000, 9, 16],
    "sa3007051": ["sa3007051", 1997, 6, 3],
    "sa3007295": ["sa3007295", 2000, 10, 1],
    "sa3007744": ["sa3007744", 2000, 12, 22],
    "sa3008139": ["sa3008139", 1997, 3, 15],
    "sa3008436": ["sa3008436", 1999, 12, 17],
    "sa3008743": ["sa3008743", 2002, 4, 26],
    "sa3008762": ["sa3008762", 2002, 1, 22],
    "sa3010022": ["sa3010022", 2001, 9, 10],
    "sa3011446": ["sa3011446", 2000, 8, 25],
    "sa3011526": ["sa3011526", 1998, 2, 4],
    "sa392969": ["sa829387", 1997, 2, 24],
    "sa915815": ["sa915815", 1996, 4, 2],
    "sa918676": ["sa918676", 1997, 12, 26],
    "sa3009873": ["sa3009873", 1998, 9, 13],
    "sa3008762": ["sa3008762", 2002, 1, 27],
    "sa874174": ["sa874174", 1994, 12, 24],
    "sa3004278": ["sa3004278", 1998, 9, 10],
    "sa828703": ["sa828703", 1996, 8, 15],
    "sa874806": ["sa874806", 1996, 9, 10],
    "sa828873": ["sa828873", 1996, 11, 18],
    "sa738514": ["sa738514", 1994, 9, 29],
    "sa917955": ["sa917955", 1996, 9, 9],
    "sa3008139": ["sa3008139", 1997, 3, 5],
    "sa3008031": ["sa3008031", 1997, 7, 8],
    
    }

    if fg_id in birthday_dict:
        fg_id2, byear, bmonth, bday = birthday_dict.get(fg_id)
        return fg_id2, byear, bmonth, bday
    else:
        return fg_id, byear, bmonth, bday


def adjust_fg_age(full_name, year, list_type, age):
    """
    Adjusts a prospect's age given their fangraphs listed age (age).
    """
    age_search = full_name + "_" + str(year) + "_" + str(list_type)

    ages_dict = {
    "Adrian Morejon_2016_international":17.3,

    }

    if age_search in ages_dict:
        age = ages_dict.get(age_search)
        return age
    else:
        return age


def adjust_minorleagueball_name(full_name, year, team_abb):
    """
    Splits a players minorleagueball full name into first and last names and returns those values.
    Also will adjust a player's name if their name has been listed non ideally so we can better match them to the professional_prospects table.
    """

    search_str = full_name.replace(" ", "") + "_" + str(year) + "_" + str(team_abb)

    names_dict = {
    'Paul"TheChairman"Voelker_2016_det': ["Paul", "Voelker"],
    "A.J.Jimenez_2013_tor": ["A.J.", "Jimenez"],
    "AdamBrettWalker_2014_min": ["Adam Brett", "Walker"],
    "AdamBrettWalker_2015_min": ["Adam Brett", "Walker"],
    "AdamBrettWalker_2016_min": ["Adam Brett", "Walker"],
    "AndersonEspinosa_2016_bos": ["Anderson", "Espinoza"],
    "AndersonEspinosa_2017_sd": ["Anderson", "Espinoza"],
    "AndersonEspinosa_2018_sd": ["Anderson", "Espinoza"],
    "AntonioSantillan_2016_cin": ["Tony", "Santillan"],
    "AustinD.Adams_2015_cle": ["Austin", "Adams"],
    "AustinL.Adams_2018_was": ["Austin", "Adams"],
    "CarlEdwardsJr_2016_chc": ["C.J.", "Edwards"],
    "CodyAlabamaReed_2018_az":["Cody","Reed"],
    "CodyBuckelRHP_2013_tex": ["Cody", "Buckel"],
    "CristianPache_2017_atl": ["Cristian", "Pache"],
    "DanteBichetteJR_2013_nyy": ["Dante", "Bichette Jr."],
    "DelinoDeShields_2013_hou": ["Delino", "DeShields Jr."],
    "DonnieDewess_2018_kc": ["Donnie", "Dewees"],
    "DwightSmithJR_2016_tor": ["Dwight", "Smith Jr."],
    "EduardoParedes.RHP_2017_laa":["Eduardo", "Paredes"],
    "FernandoTatisJr_2017_sd": ["Fernando", "Tatis Jr."],
    "FernandoTatis_2018_sd": ["Fernando", "Tatis Jr."],
    "FrancellisMontas_2015_chw": ["Frankie", "Montas"],
    "J.R.Murphy_2014_nyy": ["J.R.", "Murphy"],
    "JimmyBrasoban_2016_sd": ["Yimmy", "Brasoban"],
    "JoseIsraelGarcia_2018_cin": ["Jose Israel", "Garcia"],
    "JuanCarlosPaniagua_2013_chc": ["Juan Carlos", "Paniagua"],
    "LanceMcCullers_2013_hou": ["Lance", "McCullers Jr."],
    "LanceMcCullers_2014_hou": ["Lance", "McCullers Jr."],
    "LourdesGurriel_2017_tor": ["Lourdes", "Gurriel Jr."],
    "LuisAlexanderBasabe_2016_bos": ["Luis Alexander", "Basabe"],
    "LuisAlexanderBasabe_2017_chw": ["Luis Alexander", "Basabe"],
    "MiguelAlfredoGonzalez_2015_phi": ["Miguel Alfredo", "Gonzalez"],
    "NickFranklinSS_2013_sea": ["Nick", "Franklin"],
    "RaulAlcantaraRHP_2015_oak": ["Paul", "Alcantara"],
    "RaulMondesi_2014_kc": ["Adalberto", "Mondesi"],
    "RaulMondesi_2015_kc": ["Adalberto", "Mondesi"],
    "RaulMondesi_2016_kc": ["Adalberto", "Mondesi"],
    "TrentClark_2016_mil": ["Trent", "Grisham"],
    "TrentClark_2017_mil": ["Trent", "Grisham"],
    "TreyMicalczewski_2015_chw": ["Trey", "Michalczewski"],
    "TroyStokes_2018_mil": ["Troy", "Stokes Jr."],
    "VladGuerrero_2016_tor": ["Vladimir", "Guerrero Jr."],
    "VladimirGuerreroJr_2017_tor": ["Vladimir", "Guerrero Jr."],
    "VladimirGuerrero_2018_tor": ["Vladimir", "Guerrero Jr."],
    }

    if search_str in names_dict:
        fname, lname = names_dict.get(search_str)
        full_name = fname + " " + lname
        return full_name, fname, lname
    else:
        fname, lname = [full_name.replace("  "," ").split(" ")[0], " ".join(full_name.split(" ")[1:])]
        return full_name, fname, lname


def adjust_minorleagueball_position(full_name, year, team_abb, position):
    """
    Adjusts a prospect's position given their minorleagueball full name, year, and team.
    Used primaily to hardcode positions for player's who have had their original name parsing go astray.
    """
    search_str = full_name.replace(" ", "") + "_" + str(year) + "_" + str(team_abb)

    positions_dict = {
    "CodyBuckel_2013_tex": "RHP",
    "DelinoDeShieldsJr._2013_hou": "OF",
    "EduardoParedes_2017_laa": "RHP",
    "FernandoTatisJr._2018_sd": "3B",
    "LanceMcCullersJr._2013_hou": "RHP",
    "LanceMcCullersJr._2014_hou": "RHP",
    "LourdesGurrielJr._2017_tor": "SS",
    "NickFranklin_2013_sea": "SS",
    "RaulAlcantara_2015_oak": "RHP",
    "TroyStokesJr._2018_mil": "OF",
    "VladimirGuerreroJr._2016_tor": "3B",
    "VladimirGuerreroJr._2018_tor": "3B",
    }

    if search_str in positions_dict:
        position = positions_dict.get(search_str)

    return position


def adjust_minorleagueball_birthyear(full_name, year, team_abb, est_birthyear):
    """
    Adjusts a player's minorleagueball birthyear to better determine their age to match to the professional_prospects table.
    If no adjustment is needed, returns the original estimate for their birthyear.
    """
    search_str = full_name.replace(" ", "") + "_" + str(year) + "_" + str(team_abb)

    years_dict = {
    "AbrahamToro-Hernandez_2018_hou": 1998,
    "AnyeloGomez_2018_atl": 1993,
    "AustinBeck_2018_oak": 1998,
    "BradKeller_2018_kc": 1995,
    "CarlosTocci_2017_phi": 1996,
    "DanielPalka_2017_min": 1992,
    "FernandoRomero_2017_min": 1996,
    "HectorVelazquez_2018_bos": 1989,
    "LewisThorpe_2017_min": 1997,
    "MitchGarver_2017_min": 1992,
    "NickGordon_2017_min": 1996,
    "StephenGonsalves_2017_min": 1995,
    "WanderJavier_2017_min": 2000,
    }

    if search_str in years_dict:
        est_birthyear = years_dict.get(search_str)

    age = year - est_birthyear 
    return age


def adjust_minorleagueball_grade(full_name, year, team_abb, grade):
    """
    Adjusts a prospect's grade given their minorleagueball full name, year, team, and grade.
    If no adjustment is needed, returns the original grade.
    Used primaily to hardcode positions for player's who have had their original grade parsing go astray.
    """
    search_str = full_name.replace(" ", "") + "_" + str(year) + "_" + str(team_abb)

    grades_dict = {
    "AnthonySantander_2017_bal": "B-",
    "Chih-WeiHu_2018_tb": "B-/C+",
    "DemiOrimoloye_2016_mil": "B-/C+",
    "EmmanuelRivera_2018_kc": "C+",
    "JamesonTaillon_2014_pit": "B+",
    "MichaelRatterree_2014_mil": "C+/C",
    "SamTravis_2016_bos": "B/B-",
    "StephenGonsalves_2018_min": "B/B+",
    }

    if search_str in grades_dict:
        grade = grades_dict.get(search_str)

    return grade


def adjust_minorleagueball_eta(full_name, year, team_abb, eta):
    """
    Adjusts a prospect's eta given their minorleagueball full name, year, team, and eta.
    If no adjustment is needed, returns the original eta.
    Used primaily to hardcode positions for player's who have had their original blurb parsing go astray.
    """
    search_str = full_name.replace(" ", "") + "_" + str(year) + "_" + str(team_abb)

    eta_dict = {
    "CodySedlock_2017_bal": "late 2019, or 2018 if used in bullpen",
    "JoanGregorio_2017_sf": 2017,
    "JordanJohnson_2017_sf": 2019,
    "MaxKepler_2018_min": 2017,
    "MikeShawaryn_2017_bos": 2019,
    "MitchellWhite_2017_lad": 2019,
    }

    if search_str in eta_dict:
        eta = eta_dict.get(search_str)

    return eta


