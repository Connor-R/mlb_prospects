SHELL=/bin/bash
source "/Users/connordog/.bash_profile"

year=2020


# 2020 update - all this shit is kinda broken.
#     minorleagueball no longer exists
#     mlb.com changed their api and I didn't want to rewrite the scraper
#     so this is basically a scraper/processor of fangraphs prospect, which is better than nothing, but you could prob just download the board as a csv and be just as good


# only run this if doing a clean scrap
# python processing/prospect_db_rescrape_prep.py --end_year "$year" --delete_length "Current"

wait

python scrapers/mlb_prospect_scraper.py --end_year "$year" --scrape_length "Current"

## wait

## python processing/mlb_prospect_grades.py

wait

#truncate all fg_tables first

python scrapers/fangraphs_prospect_scraper.py --end_year "$year" --scrape_length "All"

wait

python processing/fangraphs_prospect_parser.py --end_year "$year" --scrape_length "All"

wait

# python scrapers/minorleagueball_prospect_scraper.py --end_year "$year" --scrape_length "Current"

# wait

# python processing/minorleagueball_prospect_id_grade_updater.py

wait

bash prospects_tables_run.sh

wait

python processing/fangraphs_draft_list.py