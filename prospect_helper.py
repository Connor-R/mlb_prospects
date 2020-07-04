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
        OR (fg_major_id = "%s" AND fg_major_id IS NOT NULL)
        OR (fg_temp_id = "%s" AND fg_temp_id IS NOT NULL))""" % (site_id, site_id, site_id, site_id, site_id, site_id)
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
                if "_" in site_id:
                    id_column = "fg_temp_id"
                elif site_id[0] == "s":
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
                if "_" in site_id:
                    entry["fg_temp_id"] = site_id
                elif site_id[0] == "s":
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
    player_mapper = {
    }

    qry = """SELECT wrong_name
    , right_fname
    , right_lname
    FROM name_mapper nm
    ;"""

    res = db.query(qry)
    for row in res:
        wrong, right_fname, right_lname = row
        player_mapper[wrong] = [right_fname, right_lname]


    if mlb_id in player_mapper:
        fname, lname = player_mapper.get(mlb_id)
        return fname, lname
    else:
        return fname, lname

def adjust_mlb_positions(mlb_id, position):
    """
    Adjusts a prospect's position given their mlb.com player_id (mlb_id).
    Not heavily necessary unless a player has been mis-classified as a pitcher when they should be a hitter or vice versa.
    """

    qry = db.query("SELECT position FROM z_helper_mlb_positions WHERE mlb_id = '%s';" % (mlb_id))
    if qry != ():
        position = qry[0][0]

    return position

def adjust_mlb_birthdays(mlb_id, byear, bmonth, bday):
    """
    Adjusts a prospect's birthday given their mlb.com birthdate (byear, bmonth, bday).
    Mostly used in adjusted wrong birthdates for draft prospects in earlier seasons.
    """

    qry = db.query("SELECT birth_year, birth_month, birth_day FROM z_helper_mlb_birthdays WHERE mlb_id = '%s';" % (mlb_id))
    if qry != ():
        byear, bmonth, bday = qry[0][0], qry[0][1], qry[0][2]

    return byear, bmonth, bday 

def adjust_fg_names(full_name):
    """
    Splits a players full name into first and last names and returns those values.
    Also will adjust a player's name if their name has been listed non ideally so we can better match them to the professional_prospects table.
    """

    player_mapper = {
    }

    qry = """SELECT wrong_name
    , right_fname
    , right_lname
    FROM name_mapper nm
    ;"""

    res = db.query(qry)
    for row in res:
        wrong, right_fname, right_lname = row
        player_mapper[wrong] = [right_fname, right_lname]

    if full_name in player_mapper:
        fname, lname = player_mapper.get(full_name)
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
    positions_dict = {
    }
 
    if full_name in positions_dict:
        position = positions_dict.get(full_name)
        return position
    else:
        return position

def adjust_fg_birthdays(fg_id, byear, bmonth, bday): 
    """
    Adjusts a prospect's birthday given their fangraphs birthdate (byear, bmonth, bday) and fangraphs id (fg_id).
    """

    qry = db.query("SELECT adjusted_fg_id, birth_year, birth_month, birth_day FROM z_helper_mlb_birthdays WHERE mlb_id = '%s';" % (mlb_id))
    if qry != ():
        fg_id, byear, bmonth, bday = qry[0][0], qry[0][1], qry[0][2], qry[0][3]

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

    player_mapper = {
    }

    qry = """SELECT wrong_name
    , right_fname
    , right_lname
    FROM name_mapper nm
    ;"""

    res = db.query(qry)
    for row in res:
        wrong, right_fname, right_lname = row
        player_mapper[wrong] = [right_fname, right_lname]


    if search_str in player_mapper:
        fname, lname = player_mapper.get(search_str)
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

    qry = db.query("SELECT position FROM z_helper_minorleagueball_positions WHERE minorleagueball_id = '%s';" % (search_str))
    if qry != ():
        position = qry[0][0]

    return position

def adjust_minorleagueball_birthyear(full_name, year, team_abb, est_birthyear):
    """
    Adjusts a player's minorleagueball birthyear to better determine their age to match to the professional_prospects table.
    If no adjustment is needed, returns the original estimate for their birthyear.
    """
    search_str = full_name.replace(" ", "") + "_" + str(year) + "_" + str(team_abb)

    qry = db.query("SELECT birth_year FROM z_helper_minorleagueball_birthyear WHERE minorleagueball_id = '%s';" % (search_str))
    if qry != ():
        est_birthyear = qry[0][0]

    age = year - est_birthyear 
    return age

def adjust_minorleagueball_grade(full_name, year, team_abb, grade):
    """
    Adjusts a prospect's grade given their minorleagueball full name, year, team, and grade.
    If no adjustment is needed, returns the original grade.
    Used primaily to hardcode positions for player's who have had their original grade parsing go astray.
    """
    search_str = full_name.replace(" ", "") + "_" + str(year) + "_" + str(team_abb)

    qry = db.query("SELECT grade FROM z_helper_minorleagueball_grades WHERE minorleagueball_id = '%s';" % (search_str))
    if qry != ():
        grade = qry[0][0]

    return grade

def adjust_minorleagueball_eta(full_name, year, team_abb, eta):
    """
    Adjusts a prospect's eta given their minorleagueball full name, year, team, and eta.
    If no adjustment is needed, returns the original eta.
    Used primaily to hardcode positions for player's who have had their original blurb parsing go astray.
    """
     search_str = full_name.replace(" ", "") + "_" + str(year) + "_" + str(team_abb)

    qry = db.query("SELECT eta FROM z_helper_minorleagueball_eta WHERE minorleagueball_id = '%s';" % (search_str))
    if qry != ():
        eta = qry[0][0]

    return eta
