import requests, json
from ..connection.db import get_connection

def fetch_players(season):
    r = requests.get('https://statsapi.mlb.com/api/v1/sports/1/players', params={
        'season': season
    })

    players = r.json().get("people", [])
    conn = get_connection()
    for p in players:
        try:
            conn.execute("""INSERT OR REPLACE INTO players
                         (player_id, full_name, birth_date, position, bat_side, pitch_hand)
                         VALUES (?, ?, ?, ?, ?, ?)
                         """, (
                            p["id"],
                            p.get("fullName"),
                            p.get("birthDate"),
                            p.get("primaryPosition", {}).get("abbreviation"),
                            p.get("batSide", {}).get("code"),
                            p.get("pitchHand", {}).get("code")
                        ))
        except Exception as e:
            print(f"Error inserting player {p.get('id')}: {e}")

    conn.commit()
    conn.close()
    print(f"Players fetched: {len(players)}")


if __name__ == "__main__":
    for season in [2024, 2025]:
        fetch_players(season)
        print("Season fetched ")