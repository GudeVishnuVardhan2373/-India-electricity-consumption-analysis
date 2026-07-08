"""
app.py
------
Flask app for Step 7 (Web Integration): embeds your published Tableau
Public dashboard and story in a simple website.

Setup:
1. Publish your dashboard and story to Tableau Public (Server > Publish Workbook).
2. Copy each view's embed URL from Tableau Public
   (Share button -> copy the "https://public.tableau.com/views/..." link).
3. Paste those URLs into DASHBOARD_URL and STORY_URL below.
4. pip install flask --break-system-packages
5. python app.py
6. Visit http://localhost:5000
"""

from flask import Flask, render_template

app = Flask(__name__)

# TODO: replace with your real published Tableau Public view URLs
DASHBOARD_URL = "https://public.tableau.com/views/YourWorkbookName/YourDashboardName"
STORY_URL = "https://public.tableau.com/views/YourWorkbookName/YourStoryName"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", embed_url=DASHBOARD_URL)


@app.route("/story")
def story():
    return render_template("story.html", embed_url=STORY_URL)


if __name__ == "__main__":
    app.run(debug=True)
