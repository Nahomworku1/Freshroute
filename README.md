# FreshRoute — Setup in 5 Minutes

## Step 1 — Get your free API key (2 min)
1. Go to https://openweathermap.org/api
2. Click "Sign Up" — it's free
3. Go to "API Keys" tab in your account
4. Copy your key

## Step 2 — Paste your key
Open the file: .streamlit/secrets.toml
Replace PASTE_YOUR_KEY_HERE with your actual key.

Note: the free key takes ~10 minutes to activate after signup.

## Step 3 — Install and run (open your Terminal / Command Prompt)

cd freshroute
pip install -r requirements.txt
streamlit run app.py

Your browser will open automatically at http://localhost:8501

## What's real vs simulated
- REAL: Temperature, humidity, weather conditions (live from OpenWeatherMap)
- REAL: Spoilage calculation (agricultural science formula using real weather)
- SIMULATED: Buyer database (this is FreshRoute's product — it grows with usage)
- SIMULATED: Road conditions (approximated from weather)

## For the pitch
Change the city, crop, quantity and days in the sidebar.
Use the intervention simulator to show judges the impact of each action.
The weather data updates every 5 minutes automatically.
