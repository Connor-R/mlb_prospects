SHELL=/bin/bash
source "/Users/connordog/.bash_profile"

updateDate=$( date +"%b %d, %Y" )
year=2019

python processing/master_prospect_tables.py

wait

csvtotable /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/MLB_Prospects_masterprospects.csv /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/master_prospects.html -c "MLB Prospect Dataset (via mlb.com, fangraphs.com, minorleagueball.com) (Last Updated $updateDate)" -o -vs 15
python /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/google_analytics_appender.py --file_path "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/master_prospects.html"

csvtotable /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/MLB_Prospects_mastercurrent.csv /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/master_current.html -c "MLB $year Prospect Dataset (via mlb.com, fangraphs.com, minorleagueball.com) (Last Updated $updateDate)" -o -vs 15
python /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/google_analytics_appender.py --file_path "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/master_current.html"

cd /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io
git add Tables/master_prospects.html
git add Tables/master_current.html
git add csvs/MLB_Prospects_mastercurrent.csv
git add csvs/MLB_Prospects_masterprospects.csv
git commit -m "update prospect dataset"
git push