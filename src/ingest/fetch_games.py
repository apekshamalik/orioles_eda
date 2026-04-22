import requests, json, sqlite3
from ..connection.db import get_connection

def fetch_games(season):
    r = requests.get('https://statsapi.mlb.com/api/v1/schedule', params={
        'season': season,
        'sportId': 1,
        'gameType': 'R'
    })

    dates = r.json().get("dates", [])
    conn = get_connection()
    inserted = 0

    for date in dates:
        for game in date.get("games", []):
            if game["status"]["abstractGameState"] != "Final":
               continue
            try:
                conn.execute("""INSERT OR REPLACE INTO games
                                (game_pk, game_date, season, game_type, home_team_id, away_team_id, status)
                             VALUES (?, ?, ?, ?, ?, ?, ?) 
                             """, (
                                game.get("gamePk"),
                                game.get("gameDate"),
                                int(game.get("season")),
                                game.get("gameType"),
                                game.get("teams", {}).get("home", {}).get("team", {}).get("id"),
                                game.get("teams", {}).get("away", {}).get("team", {}).get("id"),
                                game.get("status", {}).get("abstractGameState")
                             ))
                inserted += 1
            except sqlite3.Error as e:
                print(f"Error inserting game {game.get('gamePk')}: {e}")
            
    conn.commit()
    conn.close()

if __name__ == "__main__":
    for season in [2024, 2025]:
        fetch_games(season)
        print("Season fetched ")