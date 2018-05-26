SHELL=/bin/bash
source "/Users/connordog/.bash_profile"

python prospect_db_rescrape_prep.py --end_year 2018 --delete_length "Current"

wait

python mlb_prospect_scraper.py --end_year 2018 --scrape_length "Current"

wait

python mlb_prospect_grades.py

wait

python fangraphs_prospect_scraper.py --end_year 2018 --scrape_length "Current"

wait

python minorleagueball_prospect_scraper.py --end_year 2018 --scrape_length "Current"

wait

python minorleagueball_prospect_id_grade_updater.py