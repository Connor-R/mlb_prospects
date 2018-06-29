SHELL=/bin/bash
source "/Users/connordog/.bash_profile"

year=2018

python processing/prospect_db_rescrape_prep.py --end_year "$year" --delete_length "Current"

wait

python scrapers/mlb_prospect_scraper.py --end_year "$year" --scrape_length "Current"

wait

python processing/mlb_prospect_grades.py

wait

python scrapers/fangraphs_prospect_scraper.py --end_year "$year" --scrape_length "Current"

wait

python scrapers/minorleagueball_prospect_scraper.py --end_year "$year" --scrape_length "Current"

wait

python processing/minorleagueball_prospect_id_grade_updater.py

wait

python processing/fangraphs_draft_list.py