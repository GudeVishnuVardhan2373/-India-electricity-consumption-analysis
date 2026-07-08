India Electricity Consumption Analysis — Project
Full working scaffold for your Data Integration / Tableau / Data Analysis project. See docs/documentation.md for the complete step-by-step writeup mapped to all 8 project steps (this is your Step 8 documentation deliverable too — just fill in screenshots/final numbers once Tableau is built).

Quick Start
cd database
pip install pandas sqlalchemy --break-system-packages
python load_data.py          # builds consumption.db from data/Consumption.csv

cd ../analysis
pip install pandas matplotlib --break-system-packages
python eda.py                 # sanity-check charts in analysis/output/

# Build your Tableau dashboard + story against database/consumption.db
# (connect to the vw_consumption_full view), then publish to Tableau Public.

cd ../webapp
pip install flask --break-system-packages
# edit app.py: paste your Tableau Public embed URLs
python app.py                 # visit http://localhost:5000
What's Already Done For You
✅ Normalized DB schema + working ETL script (Step 1)
✅ SQL for all 3 scenarios (Step 1/2)
✅ Python EDA charts to preview what Tableau should show (Step 2/3)
✅ Flask app skeleton ready for Tableau embed (Step 7)
✅ Full documentation draft (Step 8)
What You Still Need To Do
Build the actual Tableau dashboard + story (Steps 3–5) — this part has to be done in Tableau Desktop/Public directly, it can't be scripted.
Performance-test your dashboard/story in Tableau (Step 6).
Publish to Tableau Public and paste the embed URLs into webapp/app.py (Step 7).
Record your demo video (Step 8).
