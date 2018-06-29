SHELL=/bin/bash
source "/Users/connordog/.bash_profile"

year=2018

python processing/master_prospect_tables.py

wait

csvtotable /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/masterprospects.csv /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/master_prospects.html -c "MLB Prospect Dataset (via mlb.com, fangraphs.com, minorleagueball.com)" -o -vs 15
python /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/google_analytics_appender.py --file_path "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/master_prospects.html"

csvtotable /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/mastercurrent.csv /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/master_current.html -c "MLB $year Prospect Dataset (via mlb.com, fangraphs.com, minorleagueball.com)" -o -vs 15
python /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/google_analytics_appender.py --file_path "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/master_current.html"

cd /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io
git add Tables/master_prospects.html
git add Tables/master_current.html
git add csvs/mastercurrent.csv
git add csvs/masterprospects.csv
git commit -m "update prospect dataset"
git push