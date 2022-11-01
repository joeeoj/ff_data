CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY,
    week INTEGER NOT NULL,
    home_team VARCHAR(100),
    home_score FLOAT,
    away_team VARCHAR(100),
    away_score FLOAT
);

CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY,
    txn_id VARCHAR(36),
    related_txn_id VARCHAR(36),
    week INTEGER,
    type VARCHAR(20),
    status VARCHAR(20),
    bid_amount INTEGER,
    waiver_order INTEGER,
    team_name VARCHAR(100),
    team_abbrev VARCHAR(4),
    proposed_date DATETIME,
    expiration_date DATETIME,
    move_type VARCHAR(20),
    player_name VARCHAR(50),
    from_team VARCHAR(100),
    to_team VARCHAR(100),
    from_slot VARCHAR(4),
    to_slot VARCHAR(4)
);

CREATE INDEX IF NOT EXISTS team_abbrev_idx ON transactions(team_abbrev);
CREATE INDEX IF NOT EXISTS team_name_idx ON transactions(team_name);
CREATE INDEX IF NOT EXISTS proposed_date_idx ON transactions(proposed_date);
