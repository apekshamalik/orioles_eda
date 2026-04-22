import requests, json
from ..connection.db import get_connection

def fetch_teams(season):
    r = requests.get('https://statsapi.mlb.com/api/v1/teams', params={
        'sportId': 1,
        'season': season,
        'hydrate': 'league,division'
    })

    teams = r.json()["teams"]
    conn = get_connection()
    for t in teams:
        conn.execute("""INSERT OR REPLACE INTO teams 
                     (team_id, season, name, abbreviation, league_id, league_name, division_id, division_name) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                     """, (
                        t["id"],
                        t["season"],
                        t["name"],
                        t.get("abbreviation"),
                        t.get("league", {}).get("id"),
                        t.get("league", {}).get("name"),
                        t.get("division", {}).get("id"),
                        t.get("division", {}).get("name")
                    ))
    conn.commit()
    conn.close()
    print("Teams fetched ")


if __name__ == "__main__":
    for season in [2024, 2025]:
        fetch_teams(season)
        print("Teams fetched ")