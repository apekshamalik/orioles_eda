CREATE TABLE IF NOT EXISTS teams (
    team_id     INTEGER PRIMARY KEY,
    season      INTEGER,
    name        TEXT,
    abbreviation TEXT,
    league_id   INTEGER,
    league_name TEXT,
    division_id INTEGER,
    division_name TEXT
);

CREATE TABLE IF NOT EXISTS players (
    player_id   INTEGER PRIMARY KEY,
    full_name   TEXT,
    birth_date  TEXT,
    position    TEXT,
    bat_side    TEXT,
    pitch_hand  TEXT
);

CREATE TABLE IF NOT EXISTS games (
    game_pk         INTEGER PRIMARY KEY,
    game_date       TEXT,
    season          INTEGER,
    game_type       TEXT,
    home_team_id    INTEGER,
    away_team_id    INTEGER,
    status          TEXT,
    FOREIGN KEY (home_team_id) REFERENCES teams(team_id),
    FOREIGN KEY (away_team_id) REFERENCES teams(team_id)
);

CREATE TABLE IF NOT EXISTS at_bats (
    at_bat_id       TEXT PRIMARY KEY,
    game_pk         INTEGER,
    inning          INTEGER,
    half_inning     TEXT,
    batter_id       INTEGER,
    pitcher_id      INTEGER,
    batter_team_id  INTEGER,
    pitcher_team_id INTEGER,
    result_event    TEXT,
    result_description TEXT,
    FOREIGN KEY (game_pk)    REFERENCES games(game_pk),
    FOREIGN KEY (batter_id)  REFERENCES players(player_id),
    FOREIGN KEY (pitcher_id) REFERENCES players(player_id)
);

CREATE TABLE IF NOT EXISTS pitches (
    pitch_id        TEXT PRIMARY KEY,
    at_bat_id       TEXT,
    game_pk         INTEGER,
    game_date       TEXT,
    pitcher_id      INTEGER,
    batter_id       INTEGER,
    pitcher_team_id INTEGER,
    batter_team_id  INTEGER,
    pitch_type      TEXT,
    season,         INTEGER,
    start_speed     REAL,
    end_speed       REAL,
    zone            INTEGER,
    hit_speed       REAL,
    hit_angle       REAL,
    hit_distance    REAL,
    pitch_call      TEXT,
    is_strike       INTEGER,
    FOREIGN KEY (at_bat_id)  REFERENCES at_bats(at_bat_id),
    FOREIGN KEY (game_pk)    REFERENCES games(game_pk),
    FOREIGN KEY (pitcher_id) REFERENCES players(player_id),
    FOREIGN KEY (batter_id)  REFERENCES players(player_id)
);

CREATE INDEX IF NOT EXISTS pitches_game    ON pitches(game_pk);
CREATE INDEX IF NOT EXISTS pitches_pitcher ON pitches(pitcher_id);
CREATE INDEX IF NOT EXISTS pitches_date    ON pitches(game_date);
CREATE INDEX IF NOT EXISTS pitches_speed   ON pitches(start_speed);
CREATE INDEX IF NOT EXISTS pitches_zone    ON pitches(zone);