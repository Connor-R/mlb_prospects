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

python processing/master_prospect_tables.py

wait

csvtotable /Users/connordog/Dropbox/Desktop_Files/Baseball/NSBL/_master_prospects.csv /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/master_prospects.html -c "MLB Prospect Dataset (via mlb.com, fangraphs.com, minorleagueball.com)" -o

cd /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io
git add Tables/master_prospects.html
git commit -m "update prospect dataset"
git push

wait

python processing/fangraphs_draft_list.py