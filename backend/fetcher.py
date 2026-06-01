import datetime
import pandas as pd
import requests

def get_dynamic_years():
    """Determines actuals and projections years based on the current date."""
    today = datetime.date.today()
    if today.month < 11:
        return today.year - 1, today.year
    return today.year, today.year + 1

def fetch_raw_data():
    """Fetches FanGraphs actuals and Steamer projections via the API."""
    actuals_yr, proj_yr = get_dynamic_years()

    # Actuals — FanGraphs leaderboard API
    hit_act_url = (
        f"https://www.fangraphs.com/api/leaders/major-league/data?"
        f"age=&pos=all&stats=bat&lg=all&season={actuals_yr}&season1={actuals_yr}"
        f"&ind=0&qual=0&type=8&month=0&pageitems=500000"
    )
    pit_act_url = (
        f"https://www.fangraphs.com/api/leaders/major-league/data?"
        f"age=&pos=all&stats=pit&lg=all&season={actuals_yr}&season1={actuals_yr}"
        f"&ind=0&qual=0&type=8&month=0&pageitems=500000"
    )

    # Projections — Steamer
    hit_proj_url = f"https://www.fangraphs.com/api/projections?stats=bat&pos=all&type=steamer&season={proj_yr}"
    pit_proj_url = f"https://www.fangraphs.com/api/projections?stats=pit&pos=all&type=steamer&season={proj_yr}"

    hit_actuals = pd.DataFrame(requests.get(hit_act_url).json()["data"])
    pitch_actuals = pd.DataFrame(requests.get(pit_act_url).json()["data"])
    steamer_bat = pd.DataFrame(requests.get(hit_proj_url).json())
    steamer_pit = pd.DataFrame(requests.get(pit_proj_url).json())

    return hit_actuals, pitch_actuals, steamer_bat, steamer_pit