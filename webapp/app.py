import os
import pandas as pd
from flask import Flask, render_template, request

# 1. Dynamic Path Resolution (Works perfectly on local and Render)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CSV_PATH = os.path.join(BASE_DIR, 'data', 'electricity_consumption.csv')

# 2. Get the Tableau Embed URL from Environment Variables (With a placeholder fallback)
TABLEAU_EMBED_URL = os.environ.get(
    'TABLEAU_EMBED_URL', 
    'https://public.tableau.com/views/YourWorkbookName/YourStory'  # Fallback local link
)

# 3. Initialize Flask App
app = Flask(__name__)

# 4. Safely Load CSV Data
try:
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        print("CSV loaded successfully.")
    else:
        df = None
        print(f"[Warning] CSV not found at {CSV_PATH}")
except Exception as e:
    df = None
    print(f"[Warning] Error reading CSV file: {e}")


# 5. Application Routes
@app.route('/', methods=['GET', 'HEAD'])
def index():
    if request.method == 'HEAD':
        return '', 200
        
    total_records = len(df) if df is not None else 0
    
    # Safely find the state column regardless of capitalization
    unique_states = 0
    if df is not None:
        # Find if 'State', 'state', or 'STATE' exists
        state_col = next((col for col in df.columns if col.lower() == 'state'), None)
        if state_col:
            unique_states = df[state_col].nunique()
            
    return render_template(
        'index.html', 
        tableau_url=TABLEAU_EMBED_URL,
        total_records=total_records,
        unique_states=unique_states
    )

# 6. Run Configuration (Ensures the port dynamically binds on Render)
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
