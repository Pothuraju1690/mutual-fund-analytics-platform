import requests
import pandas as pd
from datetime import datetime

print("=" * 60)
print("LIVE NAV FETCH")
print("=" * 60)

url = "https://api.mfapi.in/mf/119551"

response = requests.get(url)

if response.status_code == 200:

    data = response.json()

    scheme_name = data["meta"]["scheme_name"]
    amfi_code = data["meta"]["scheme_code"]

    latest_nav = data["data"][0]["nav"]
    latest_date = data["data"][0]["date"]

    print(f"Scheme Name : {scheme_name}")
    print(f"AMFI Code   : {amfi_code}")
    print(f"Latest NAV  : {latest_nav}")
    print(f"NAV Date    : {latest_date}")

    nav_df = pd.DataFrame([{
        "amfi_code": amfi_code,
        "scheme_name": scheme_name,
        "latest_nav": latest_nav,
        "nav_date": latest_date,
        "fetched_at": datetime.now()
    }])

    nav_df.to_csv(
        "data/processed/live_nav_data.csv",
        index=False
    )

    print("\nSUCCESS")
    print("Live NAV saved to data/processed/live_nav_data.csv")

else:
    print("Failed to fetch NAV data")