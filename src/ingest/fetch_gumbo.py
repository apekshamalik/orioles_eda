import requests, json, time, os
from ..connection.db import get_connection

CHECKPOINT_FILE = "completed_games.txt"

def load_checkpoint():
    if not os.path.exists(CHECKPOINT_FILE):
        return set()
    with open(CHECKPOINT_FILE) as f:
        return set(int(line.strip()) for line in f if line.strip())

def save_checkpoint(game_pk):
    with open(CHECKPOINT_FILE, "a") as f:
        f.write(f"{game_pk}\n")

def fetch_gumbo(game_pk, season, game_date, home_team_id, away_team_id):
    response = requests.get(f'https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live')
    if response.status_code != 200:
        print(f"Failed to fetch game {game_pk}: {response.status_code}")
        return

    data = response.json()
    plays = data.get("liveData", {}).get("plays", {}).get("allPlays", [])

    conn = get_connection()
    try:
        for play in plays:

            at_bat_index = play["atBatIndex"]
            at_bat_id = f"{game_pk}_{at_bat_index}"
            batter_id = play.get("matchup", {}).get("batter", {}).get("id")
            pitcher_id = play.get("matchup", {}).get("pitcher", {}).get("id")

            # get team ids from runners/matchup if available
            if play["about"]["halfInning"] == "top":
                batter_team_id  = away_team_id
                pitcher_team_id = home_team_id
            else:
                batter_team_id  = home_team_id
                pitcher_team_id = away_team_id

            try:
                conn.execute("""INSERT OR REPLACE INTO at_bats
                             (at_bat_id, game_pk, inning, half_inning, batter_id, 
                              pitcher_id, batter_team_id, pitcher_team_id, 
                              result_event, result_description)
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                             """, (
                                at_bat_id,
                                game_pk,
                                play["about"]["inning"],
                                play["about"]["halfInning"],
                                batter_id,
                                pitcher_id,
                                batter_team_id,
                                pitcher_team_id,
                                play.get("result", {}).get("event"),
                                play.get("result", {}).get("description")
                            ))
            except Exception as e:
                print(f"Error inserting at_bat {at_bat_id}: {e}")
                continue

            for event in play.get("playEvents", []):
                if not event.get("isPitch", False):
                    continue

                pitch_number = event.get("pitchNumber")
                pitch_id = f"{game_pk}_{at_bat_index}_{pitch_number}"
                pitch_data = event.get("pitchData", {})
                hit_data = event.get("hitData", {})
                details = event.get("details", {})

                try:
                    conn.execute("""INSERT OR REPLACE INTO pitches
                                 (pitch_id, at_bat_id, game_pk, game_date, season,
                                  pitcher_id, batter_id,
                                  pitcher_team_id, batter_team_id,
                                  pitch_type, start_speed, end_speed, zone,
                                  hit_speed, hit_angle, hit_distance,
                                  pitch_call, is_strike)
                                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                 """, (
                                    pitch_id,
                                    at_bat_id,
                                    game_pk,
                                    game_date,
                                    season,
                                    pitcher_id,
                                    batter_id,
                                    pitcher_team_id,
                                    batter_team_id,
                                    details.get("type", {}).get("code"),
                                    pitch_data.get("startSpeed"),
                                    pitch_data.get("endSpeed"),
                                    pitch_data.get("zone"),
                                    hit_data.get("launchSpeed"),
                                    hit_data.get("launchAngle"),
                                    hit_data.get("totalDistance"),
                                    details.get("call", {}).get("code"),
                                    1 if details.get("isStrike") else 0
                                ))
                except Exception as e:
                    print(f"Error inserting pitch {pitch_id}: {e}")

        conn.commit()
    finally:
        conn.close()
        
if __name__ == "__main__":
    completed = load_checkpoint()
    
    conn = get_connection()
    games = conn.execute(
        "SELECT game_pk, game_date, season, home_team_id, away_team_id FROM games ORDER BY game_date ASC"
    ).fetchall()
    conn.close()

    total = len(games)
    processed = 0
    for game in games:
        game_pk = game["game_pk"]

        if game_pk in completed:
            print(f"Skipping {game_pk} (already done)")
            continue

        processed += 1
        print(f"[{processed}/{total}] Fetching game {game_pk} ({game['game_date']})...")
        try:
            fetch_gumbo(
                game_pk,
                game["season"],
                game["game_date"],
                game["home_team_id"],
                game["away_team_id"]
            )
            save_checkpoint(game_pk)
        except Exception as e:
            print(f"Failed on game {game_pk}: {e}")

        time.sleep(1)
