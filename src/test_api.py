import requests
import json

# Gamepks to unlock other api schemas
r = requests.get("https://statsapi.mlb.com/api/v1/schedule", params={
    "sportId": 1,
    "season": 2024,
    "gameType": "R"
})
data = r.json()
if data.get("dates"):
    games = data["dates"][0].get("games", [])[:5]
else:
    games = []
for g in games:
    print(g["gamePk"], g["gameDate"], g["status"]["abstractGameState"])

# Test 2: pull one GUMBO feed and look at one pitch
game_pk = games[0]["gamePk"]
r2 = requests.get(f"https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live")
gumbo = r2.json()

plays = gumbo["liveData"]["plays"]["allPlays"]
for play in plays[:3]:
    for event in play.get("playEvents", []):
        if "pitchData" in event:
            print(json.dumps(event["pitchData"], indent=2))
            break
    break