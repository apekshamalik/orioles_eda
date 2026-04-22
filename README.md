# orioles_eda

MLB Stats API → SQLite pipeline.
a small data pipeline that pulls MLB game data from the Stats API and stores it in a SQLite database for analysis. 

collects basic game information, then uses the GUMBO feed to break each game down into at-bats and individual pitches. the goal is to take nested PA and pitch data and turn it into a queryable relational dataset.
